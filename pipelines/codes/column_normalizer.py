"""
column_normalizer.py
--------------------
Handles column name normalization for pharmacy-uploaded CSV files.

Pipeline:
    Step 1 → Lowercase & strip all column names
    Step 2 → Exact match from mapping dictionary
    Step 3 → Fuzzy match fallback (rapidfuzz)
    Step 4 → Drop columns not in our schema
    Step 5 → Flag any expected columns that are missing

Dependencies:
    pip install pandas rapidfuzz

SCHEMA MIGRATION NOTES (new ERD)
─────────────────────────────────────────────────────────────
  - TABLE_SCHEMAS["drug_prices"] renamed → "pharmacy_inventory"
      Removed:  available, name
      Added:    quantity, minimum_stock

  - TABLE_SCHEMAS["drugs"]
      Renamed:  active_ingredient → active_substance
      Added:    dosage_form, strength, manufacturer, image_url

  - TABLE_SCHEMAS["drug_categories"]
      Added:    description

  - COLUMN_MAPPING
      All "active_ingredient" target values renamed → "active_substance"
      New sections added for: active_substance, dosage_form, strength,
                              manufacturer, image_url, quantity, minimum_stock

  NOTE — PK columns (id) are intentionally excluded from TABLE_SCHEMAS.
  The normalizer is called on pharmacy-uploaded CSVs only.
  Structured CSVs (drugs.csv, drug_categories.csv, drug_alternatives.csv)
  are copied directly to seeds/ without normalization and must already
  use the correct ERD column names.

  NOTE — "available" entries in COLUMN_MAPPING are kept for backward
  compatibility with old pharmacy CSVs. Since "available" is no longer
  in the pharmacy_inventory schema, it is silently dropped at Step 4.

  NOTE — pharmacy_inventory no longer includes "name". Per the ERD,
  pharmacies upload drug_id directly (an internal ID they already know),
  not a drug name. This removed the entire name → drug_id resolution
  step that previously existed in core_pharmacy_inventory.sql, and also
  removed the "auto-add unknown drug" branch from core_drugs.sql, since
  there is no longer a name to auto-catalogue an unknown drug from.
  Any inventory row with a drug_id not found in core_drugs is now
  dropped (not auto-added) — this is an intentional decision, not an
  oversight, confirmed as part of this migration.
  ASSUMPTION (to be revisited): this assumes pharmacies — or whatever
  system sits between them and our pipeline — resolve drug names to our
  internal drug_id before the file reaches Supabase Storage. If that is
  not actually true in production, this file and the core model both
  need to be revisited.
"""

import pandas as pd
from rapidfuzz import process
import logging

# ─────────────────────────────────────────────
# Logging setup
# ─────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────
# Schema Definitions
# What columns each table expects (standard names)
#
# PK columns (id) are excluded by design — see module docstring.
# ─────────────────────────────────────────────
TABLE_SCHEMAS = {
    "drugs": [
        "name",
        "active_substance",     # renamed from active_ingredient
        "category_id",
        "dosage_form",          # new
        "strength",             # new
        "manufacturer",         # new
        "description",
        "image_url",            # new
    ],
    "pharmacy_inventory": [     # renamed from drug_prices
        "pharmacy_id",
        "drug_id",               # pharmacies upload internal drug_id directly (per ERD)
        "quantity",              # new — replaces available; availability = quantity > 0
        "minimum_stock",         # new
        "price",
        "last_updated",
    ],
    "drug_categories": [
        "name",
        "description",          # new
    ],
    "drug_alternatives": [
        "drug_id",
        "alternative_drug_id"
    ]
}


# ─────────────────────────────────────────────
# Column Mapping Dictionary
# Maps all known variations → standard column name
# Add new variations here as you discover them
# ─────────────────────────────────────────────
COLUMN_MAPPING = {

    # ── Drug name variations ──
    "drug_name":                "name",
    "medical_name":             "name",
    "medicine_name":            "name",
    "medication_name":          "name",
    "medication":               "name",
    "drug":                     "name",
    "trade_name":               "name",
    "brand_name":               "name",
    "product_name":             "name",
    "item_name":                "name",

    # ── Active substance variations ──
    # (previously mapped to "active_ingredient" — renamed to "active_substance")
    "active_substance":         "active_substance",
    "active_ingredient":        "active_substance",
    "ingredient":               "active_substance",
    "generic_name":             "active_substance",
    "compound":                 "active_substance",
    "formula":                  "active_substance",
    "chemical_name":            "active_substance",
    "composition":              "active_substance",
    "active_compound":          "active_substance",
    "main_ingredient":          "active_substance",

    # ── Dosage form variations ── (new)
    "dosage_form":              "dosage_form",
    "form":                     "dosage_form",
    "drug_form":                "dosage_form",
    "formulation":              "dosage_form",
    "drug_formulation":         "dosage_form",
    "pharmaceutical_form":      "dosage_form",

    # ── Strength variations ── (new)
    "strength":                 "strength",
    "dosage":                   "strength",
    "concentration":            "strength",
    "potency":                  "strength",
    "dose":                     "strength",
    "drug_strength":            "strength",

    # ── Manufacturer variations ── (new)
    "manufacturer":             "manufacturer",
    "made_by":                  "manufacturer",
    "company":                  "manufacturer",
    "pharma_company":           "manufacturer",
    "produced_by":              "manufacturer",
    "drug_manufacturer":        "manufacturer",
    "producing_company":        "manufacturer",

    # ── Image URL variations ── (new)
    "image_url":                "image_url",
    "image":                    "image_url",
    "photo_url":                "image_url",
    "picture_url":              "image_url",
    "img_url":                  "image_url",
    "drug_image":               "image_url",

    # ── Category variations ──
    "category_id":              "category_id",
    "category":                 "category_id",
    "drug_category":            "category_id",
    "drug_type":                "category_id",
    "type":                     "category_id",
    "class":                    "category_id",
    "drug_class":               "category_id",

    # ── Description variations ──
    "description":              "description",
    "desc":                     "description",
    "details":                  "description",
    "drug_description":         "description",
    "notes":                    "description",
    "info":                     "description",

    # ── Price variations ──
    "price":                    "price",
    "drug_price":               "price",
    "cost":                     "price",
    "amount":                   "price",
    "unit_price":               "price",
    "selling_price":            "price",
    "retail_price":             "price",
    "sale_price":               "price",

    # ── Quantity variations ── (new — replaces available as the inventory signal)
    "quantity":                 "quantity",
    "qty":                      "quantity",
    "stock":                    "quantity",
    "stock_quantity":           "quantity",
    "stock_level":              "quantity",
    "current_stock":            "quantity",
    "units_available":          "quantity",
    "units_in_stock":           "quantity",
    "in_hand":                  "quantity",
    "on_hand":                  "quantity",

    # ── Minimum stock variations ── (new)
    "minimum_stock":            "minimum_stock",
    "min_stock":                "minimum_stock",
    "min_qty":                  "minimum_stock",
    "min_quantity":             "minimum_stock",
    "reorder_level":            "minimum_stock",
    "reorder_point":            "minimum_stock",
    "safety_stock":             "minimum_stock",
    "minimum_quantity":         "minimum_stock",

    # ── Availability variations ──
    # NOTE: "available" is no longer a column in pharmacy_inventory.
    # These mappings are kept for backward compatibility with old pharmacy CSVs.
    # If a CSV contains any of these columns they will be mapped to "available"
    # and then silently dropped at Step 4 (not in schema → not kept).
    "available":                "available",
    "is_available":             "available",
    "availability":             "available",
    "in_stock":                 "available",
    "stock_status":             "available",
    "status":                   "available",
    "stocked":                  "available",

    # ── Pharmacy ID variations ──
    "pharmacy_id":              "pharmacy_id",
    "pharmacy":                 "pharmacy_id",
    "branch_id":                "pharmacy_id",
    "store_id":                 "pharmacy_id",
    "branch":                   "pharmacy_id",

    # ── Drug ID variations ──
    # Used as an FK reference in pharmacy_inventory CSVs.
    # Not the same as the PK "id" column in the drugs table.
    "drug_id":                  "drug_id",
    "medicine_id":              "drug_id",
    "medication_id":            "drug_id",
    "item_id":                  "drug_id",
    "product_id":               "drug_id",

    # ── Timestamp variations ──
    "last_updated":             "last_updated",
    "updated_at":               "last_updated",
    "last_update":              "last_updated",
    "update_date":              "last_updated",
    "modified_at":              "last_updated",
    "date_modified":            "last_updated",
    "timestamp":                "last_updated",
}


# ─────────────────────────────────────────────
# STEP 1: Lowercase & strip column names
# ─────────────────────────────────────────────
def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Lowercase all column names and strip whitespace.
    Also replaces spaces with underscores for consistency.
    """
    df.columns = (
        df.columns
        .str.lower()
        .str.strip()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )
    logger.info(f"Step 1 ✅ | Cleaned column names: {list(df.columns)}")
    return df


# ─────────────────────────────────────────────
# STEP 2: Exact match from mapping dictionary
# ─────────────────────────────────────────────
def exact_match(df: pd.DataFrame) -> tuple[pd.DataFrame, list]:
    """
    Renames columns using exact matches from COLUMN_MAPPING.
    Returns the dataframe and a list of columns that had no exact match.
    """
    rename_map = {}
    unmatched = []

    for col in df.columns:
        if col in COLUMN_MAPPING:
            rename_map[col] = COLUMN_MAPPING[col]
        else:
            unmatched.append(col)

    df = df.rename(columns=rename_map)

    if rename_map:
        logger.info(f"Step 2 ✅ | Exact matches found: {rename_map}")
    if unmatched:
        logger.warning(f"Step 2 ⚠️  | No exact match for columns: {unmatched}")

    return df, unmatched


# ─────────────────────────────────────────────
# STEP 3: Fuzzy match fallback
# ─────────────────────────────────────────────
def fuzzy_match(
    df: pd.DataFrame,
    unmatched_cols: list,
    threshold: int = 80
) -> pd.DataFrame:
    """
    Tries to match unmatched columns to standard names using fuzzy matching.
    Only renames if similarity score >= threshold (default 80%).
    """
    standard_names = list(set(COLUMN_MAPPING.values()))
    rename_map = {}

    for col in unmatched_cols:
        result = process.extractOne(col, standard_names)

        if result is None:
            logger.warning(f"Step 3 ❌ | Could not fuzzy match: '{col}' — will be dropped")
            continue

        match, score, _ = result

        if score >= threshold:
            rename_map[col] = match
            logger.info(f"Step 3 ✅ | Fuzzy matched: '{col}' → '{match}' (score: {score})")
        else:
            logger.warning(
                f"Step 3 ❌ | Low confidence for '{col}' "
                f"(best match: '{match}', score: {score}) — will be dropped"
            )

    df = df.rename(columns=rename_map)
    return df


# ─────────────────────────────────────────────
# STEP 4: Drop columns not in schema
# ─────────────────────────────────────────────
def drop_extra_columns(df: pd.DataFrame, table_name: str) -> pd.DataFrame:
    """
    Keeps only the columns defined in the target table schema.
    Drops everything else.
    """
    expected_cols = TABLE_SCHEMAS.get(table_name)

    if expected_cols is None:
        raise ValueError(
            f"Unknown table: '{table_name}'. "
            f"Available tables: {list(TABLE_SCHEMAS.keys())}"
        )

    cols_to_keep = [col for col in expected_cols if col in df.columns]
    dropped = [col for col in df.columns if col not in expected_cols]

    if dropped:
        logger.info(f"Step 4 🗑️  | Dropping extra columns: {dropped}")

    df = df[cols_to_keep]
    logger.info(f"Step 4 ✅ | Kept columns: {list(df.columns)}")
    return df


# ─────────────────────────────────────────────
# STEP 5: Flag missing expected columns
# ─────────────────────────────────────────────
def flag_missing_columns(df: pd.DataFrame, table_name: str) -> dict:
    """
    Checks which expected columns are missing from the final dataframe.
    Returns a report dictionary.
    """
    expected_cols = TABLE_SCHEMAS.get(table_name, [])
    missing = [col for col in expected_cols if col not in df.columns]
    present = [col for col in expected_cols if col in df.columns]

    report = {
        "table":    table_name,
        "present":  present,
        "missing":  missing,
        "status":   "OK" if not missing else "INCOMPLETE"
    }

    if missing:
        logger.warning(
            f"Step 5 ⚠️  | Table '{table_name}' is missing expected columns: {missing}"
        )
    else:
        logger.info(f"Step 5 ✅ | All expected columns present for table '{table_name}'")

    return report


# ─────────────────────────────────────────────
# MAIN FUNCTION — Full pipeline
# ─────────────────────────────────────────────
def normalize_pharmacy_csv(
    filepath: str,
    table_name: str,
    fuzzy_threshold: int = 80
) -> tuple[pd.DataFrame, dict]:
    """
    Full normalization pipeline for a pharmacy-uploaded CSV file.

    Args:
        filepath        : Path to the uploaded CSV file
        table_name      : Target table name (must be in TABLE_SCHEMAS)
        fuzzy_threshold : Minimum fuzzy match score (0-100), default 80

    Returns:
        df      : Cleaned, normalized DataFrame ready for DuckDB
        report  : Summary report of the normalization process
    """
    logger.info(f"{'─'*55}")
    logger.info(f"🚀 Starting normalization for table: '{table_name}'")
    logger.info(f"📂 File: {filepath}")
    logger.info(f"{'─'*55}")

    # Load CSV
    df = pd.read_csv(filepath)
    logger.info(f"📋 Loaded {len(df)} rows, {len(df.columns)} columns")

    # Step 1
    df = clean_column_names(df)

    # Step 2
    df, unmatched = exact_match(df)

    # Step 3
    if unmatched:
        df = fuzzy_match(df, unmatched, threshold=fuzzy_threshold)

    # Step 4
    df = drop_extra_columns(df, table_name)

    # Step 5
    report = flag_missing_columns(df, table_name)

    logger.info(f"{'─'*55}")
    logger.info(f"✅ Normalization complete | Status: {report['status']}")
    logger.info(f"{'─'*55}\n")

    return df, report


# ─────────────────────────────────────────────
# Example usage
# ─────────────────────────────────────────────
if __name__ == "__main__":

    import os

    # ── Example 1: drugs CSV with non-standard column names ────
    print("=" * 55)
    print("Example 1 — drugs table")
    print("=" * 55)

    drugs_sample = {
        "drug_name":        ["Panadol", "Aspirin", "Amoxil"],
        "generic_name":     ["Paracetamol", "Acetylsalicylic acid", "Amoxicillin"],
        "drug_category":    [1, 2, 3],
        "formulation":      ["Tablet", "Tablet", "Capsule"],     # → dosage_form
        "concentration":    ["500mg", "100mg", "250mg"],         # → strength
        "company":          ["GSK", "Bayer", "GSK"],             # → manufacturer
        "drug_description": ["Pain reliever", "Blood thinner", "Antibiotic"],
        "extra_col":        ["x", "y", "z"],                     # → dropped
    }

    drugs_df = pd.DataFrame(drugs_sample)
    drugs_df.to_csv("/tmp/sample_drugs.csv", index=False)

    clean_df, report = normalize_pharmacy_csv(
        filepath="/tmp/sample_drugs.csv",
        table_name="drugs"
    )

    print("\n── Normalized DataFrame ──")
    print(clean_df)
    print("\n── Report ──")
    print(report)

    # ── Example 2: pharmacy inventory CSV ──────────────────────
    print("\n" + "=" * 55)
    print("Example 2 — pharmacy_inventory table")
    print("=" * 55)

    inventory_sample = {
        "pharmacy_id":  [10, 10, 10],
        "drug_id":      [1, 2, 3],                            # pharmacies upload internal drug_id directly
        "cost":         [25.50, 15.00, 45.00],                # → price
        "stock":        [100, 50, 0],                         # → quantity
        "safety_stock": [20, 10, 5],                          # → minimum_stock
        "timestamp":    ["2026-06-01", "2026-06-01", "2026-06-01"],  # → last_updated
        "is_available": [True, True, False],                  # → available (dropped, no longer in schema)
        "extra_col":    ["x", "y", "z"],                      # → dropped
    }

    inventory_df = pd.DataFrame(inventory_sample)
    inventory_df.to_csv("/tmp/sample_inventory.csv", index=False)

    clean_df2, report2 = normalize_pharmacy_csv(
        filepath="/tmp/sample_inventory.csv",
        table_name="pharmacy_inventory"
    )

    print("\n── Normalized DataFrame ──")
    print(clean_df2)
    print("\n── Report ──")
    print(report2)

    # Cleanup
    os.remove("/tmp/sample_drugs.csv")
    os.remove("/tmp/sample_inventory.csv")

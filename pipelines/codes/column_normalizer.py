"""
column_normalizer.py
--------------------
Validates and prepares pharmacy-uploaded CSV files for seeding into DuckDB.

ARCHITECTURAL CHANGE (post-incident)
─────────────────────────────────────────────────────────────
Column name normalization (exact matching + fuzzy matching via rapidfuzz)
has been REMOVED from this pipeline entirely.

Reason: fuzzy matching caused a real production incident. A bare "id"
column (the CSV's own row identity, deliberately not part of any target
schema) scored a 90% fuzzy-match confidence against "drug_id" (and,
depending on set() ordering, sometimes "pharmacy_id") purely because
"id" is a substring of both. This silently renamed the column, created
a DataFrame with two identically-labeled columns, and resulted in
pharmacy_id values being silently overwritten by row-identity values
with no error raised anywhere in the pipeline.

The correct fix is architectural, not a smarter fuzzy-match threshold:
schema correctness is now enforced upstream, before a file ever reaches
Supabase Storage —
    1. The frontend instructs pharmacies to upload files in a
       predefined, fixed schema.
    2. The backend validates the uploaded file's schema before
       forwarding it to Supabase Storage.

By the time a file reaches this pipeline, its column names are
guaranteed correct by contract. This module's job has shrunk
accordingly: read the CSV, stamp it with a processing timestamp,
verify the contract was honored, and pass clean data downstream.
It no longer guesses at intent — if the contract is violated, this
module fails loudly rather than silently repairing or dropping data.

Pipeline (current):
    Step 1 → Insert last_updated processing timestamp
    Step 2 → Drop any unexpected columns (contract violation — logged
              as an error, not silently tolerated)
    Step 3 → Verify all expected columns are present; hard-fail if not

Dependencies:
    pip install pandas
    (rapidfuzz is no longer required by this module)
"""

import pandas as pd
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
# What columns each table expects (standard, exact names).
# These are now a CONTRACT enforced upstream by the frontend/backend,
# not a target for fuzzy guessing. A file that doesn't match this
# exactly indicates the contract was violated somewhere upstream.
#
# PK columns (id) are intentionally excluded — see module docstring.
# ─────────────────────────────────────────────
NECESSARY_TABLE_SCHEMAS = {
    "drugs": [
        "name",
        "active_substance",
        "category_id",
        "dosage_form",
        "strength",
        "manufacturer",
        "description",
        "image_url",
    ],
    "pharmacy_inventory": [
        "pharmacy_id",
        "drug_id",
        "quantity",
        "minimum_stock",
        "price",
        "last_updated",
    ],
    "drug_categories": [
        "name",
        "description",
    ],
    "drug_alternatives": [
        "drug_id",
        "alternative_drug_id"
    ]
}


# ─────────────────────────────────────────────
# STEP 1: Insert last_updated processing timestamp
# ─────────────────────────────────────────────
def insert_last_updated(df: pd.DataFrame) -> pd.DataFrame:
    """
    Stamps every row with the current processing time. Pharmacy CSVs
    do not include this column — it is the pipeline's responsibility,
    reflecting the moment this file was processed (not when the
    pharmacy itself last updated their stock).

    Whole-second precision is used deliberately (no microseconds).
    Microsecond-precision timestamps have previously caused DuckDB's
    CSV sniffer to fail entirely on otherwise well-formed files.
    """
    df["last_updated"] = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Step 1 ✅ | Inserted last_updated timestamp: {df['last_updated'].iloc[0]}")
    return df


# ─────────────────────────────────────────────
# STEP 2: Drop unexpected columns
# ─────────────────────────────────────────────
def drop_extra_columns(df: pd.DataFrame, table_name: str) -> pd.DataFrame:
    """
    Keeps only the columns defined in the target table schema.
    Drops everything else.

    Under the new upstream-validated contract, this should rarely find
    anything to drop. If it does, that is a signal the frontend/backend
    schema contract was violated somewhere — logged as an error, not
    a routine cleanup step.
    """
    expected_cols = NECESSARY_TABLE_SCHEMAS.get(table_name)

    if expected_cols is None:
        raise ValueError(
            f"Unknown table: '{table_name}'. "
            f"Available tables: {list(NECESSARY_TABLE_SCHEMAS.keys())}"
        )

    cols_to_keep = [col for col in expected_cols if col in df.columns]
    dropped = [col for col in df.columns if col not in expected_cols]

    if dropped:
        logger.error(
            f"Step 2 🚨 | Unexpected columns found and dropped: {dropped}. "
            f"This indicates the upstream schema contract was violated — "
            f"investigate the frontend/backend validation for this upload."
        )

    df = df[cols_to_keep]

    # Defensive check: if selection ever produces duplicate column
    # labels, fail loudly rather than silently operating on ambiguous
    # data. This is exactly the failure mode that caused the incident
    # described in the module docstring.
    duplicate_cols = df.columns[df.columns.duplicated()].tolist()
    if duplicate_cols:
        raise ValueError(
            f"Step 2 🚨 FATAL | Duplicate column labels detected after "
            f"filtering: {duplicate_cols}. Refusing to proceed — this "
            f"would silently corrupt data. File: table '{table_name}'."
        )

    logger.info(f"Step 2 ✅ | Kept columns: {list(df.columns)}")
    return df


# ─────────────────────────────────────────────
# STEP 3: Verify expected columns are present (hard fail)
# ─────────────────────────────────────────────
def verify_schema(df: pd.DataFrame, table_name: str) -> dict:
    """
    Checks that all expected columns are present in the DataFrame.

    Per the new contract, a missing column is NOT tolerated — it means
    the upstream schema validation (frontend/backend) failed to catch
    a malformed upload, or the contract itself has drifted out of sync
    with this pipeline. Either way, this is a hard failure, not a
    warning to route around silently.

    Raises:
        ValueError if any expected column is missing.

    Returns:
        report dict, for logging purposes, if validation passes.
    """
    expected_cols = NECESSARY_TABLE_SCHEMAS.get(table_name, [])
    missing = [col for col in expected_cols if col not in df.columns]
    present = [col for col in expected_cols if col in df.columns]

    report = {
        "table":    table_name,
        "present":  present,
        "missing":  missing,
        "status":   "OK" if not missing else "REJECTED",
    }

    if missing:
        logger.error(
            f"Step 3 🚨 FATAL | Table '{table_name}' is missing required "
            f"columns: {missing}. Upstream schema contract was violated — "
            f"this file must be rejected, not silently patched."
        )
        raise ValueError(
            f"Schema contract violation for table '{table_name}': "
            f"missing required columns {missing}. Expected exactly: "
            f"{expected_cols}."
        )

    logger.info(f"Step 3 ✅ | All expected columns present for table '{table_name}'")
    return report


# ─────────────────────────────────────────────
# MAIN FUNCTION — Full pipeline
# ─────────────────────────────────────────────
def normalize_pharmacy_csv(
    filepath: str,
    table_name: str,
) -> tuple[pd.DataFrame, dict]:
    """
    Validates and prepares a pharmacy-uploaded CSV file for seeding.

    Args:
        filepath   : Path to the uploaded CSV file
        table_name : Target table name (must be in NECESSARY_TABLE_SCHEMAS)

    Returns:
        df      : Cleaned DataFrame ready for DuckDB, columns matching
                  the target schema exactly.
        report  : Summary report of the validation process.

    Raises:
        ValueError if the file violates the schema contract (missing
        required columns, or a duplicate-column condition is detected).
        Callers (e.g. the Airflow DAG) should treat this as a file to
        reject/quarantine, not a row to patch around.
    """
    logger.info(f"{'─'*55}")
    logger.info(f"🚀 Starting validation for table: '{table_name}'")
    logger.info(f"📂 File: {filepath}")
    logger.info(f"{'─'*55}")

    # Load CSV
    df = pd.read_csv(filepath)
    logger.info(f"📋 Loaded {len(df)} rows, {len(df.columns)} columns")

    # Step 1
    df = insert_last_updated(df)

    # Step 2
    df = drop_extra_columns(df, table_name)

    # Step 3 — raises on failure
    report = verify_schema(df, table_name)

    logger.info(f"{'─'*55}")
    logger.info(f"✅ Validation complete | Status: {report['status']}")
    logger.info(f"{'─'*55}\n")

    return df, report


# ─────────────────────────────────────────────
# Example usage
# ─────────────────────────────────────────────
if __name__ == "__main__":

    import os

    # ── Example 1: drugs CSV, already schema-correct ────
    print("=" * 55)
    print("Example 1 — drugs table (schema-correct upload)")
    print("=" * 55)

    drugs_sample = {
        "name":             ["Panadol", "Aspirin", "Amoxil"],
        "active_substance": ["Paracetamol", "Acetylsalicylic acid", "Amoxicillin"],
        "category_id":      [1, 2, 3],
        "dosage_form":      ["Tablet", "Tablet", "Capsule"],
        "strength":         ["500mg", "100mg", "250mg"],
        "manufacturer":     ["GSK", "Bayer", "GSK"],
        "description":      ["Pain reliever", "Blood thinner", "Antibiotic"],
        "image_url":        ["", "", ""],
    }

    drugs_df = pd.DataFrame(drugs_sample)
    drugs_df.to_csv("/tmp/sample_drugs.csv", index=False)

    clean_df, report = normalize_pharmacy_csv(
        filepath="/tmp/sample_drugs.csv",
        table_name="drugs"
    )

    print("\n── Validated DataFrame ──")
    print(clean_df)
    print("\n── Report ──")
    print(report)

    # ── Example 2: pharmacy inventory CSV, already schema-correct ──
    print("\n" + "=" * 55)
    print("Example 2 — pharmacy_inventory table (schema-correct upload)")
    print("=" * 55)

    inventory_sample = {
        "pharmacy_id":  [10, 10, 10],
        "drug_id":      [1, 2, 3],
        "price":        [25.50, 15.00, 45.00],
        "quantity":     [100, 50, 0],
        "minimum_stock":[20, 10, 5],
    }

    inventory_df = pd.DataFrame(inventory_sample)
    inventory_df.to_csv("/tmp/sample_inventory.csv", index=False)

    clean_df2, report2 = normalize_pharmacy_csv(
        filepath="/tmp/sample_inventory.csv",
        table_name="pharmacy_inventory"
    )

    print("\n── Validated DataFrame ──")
    print(clean_df2)
    print("\n── Report ──")
    print(report2)

    # ── Example 3: a file that VIOLATES the contract (extra + missing) ──
    print("\n" + "=" * 55)
    print("Example 3 — pharmacy_inventory table (contract VIOLATION)")
    print("=" * 55)

    bad_sample = {
        "id":           [1, 2, 3],   # ← unexpected column (the exact incident)
        "pharmacy_id":  [10, 10, 10],
        "drug_id":      [1, 2, 3],
        "price":        [25.50, 15.00, 45.00],
        # quantity and minimum_stock are MISSING entirely
    }

    bad_df = pd.DataFrame(bad_sample)
    bad_df.to_csv("/tmp/sample_bad.csv", index=False)

    try:
        normalize_pharmacy_csv(
            filepath="/tmp/sample_bad.csv",
            table_name="pharmacy_inventory"
        )
    except ValueError as e:
        print(f"\n✅ Correctly rejected malformed file:\n{e}")

    # Cleanup
    os.remove("/tmp/sample_drugs.csv")
    os.remove("/tmp/sample_inventory.csv")
    os.remove("/tmp/sample_bad.csv")

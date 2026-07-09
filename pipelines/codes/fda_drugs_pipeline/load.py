"""
fda_drugs_pipeline/load.py
----------------------------
Incremental, insert-only load of candidate drugs into the Neon
PostgreSQL `drugs` table.

Rules (per project owner):
  - Insert only drugs that do not already exist (matched by
    LOWER(TRIM(name)), case-insensitive).
  - Never update or delete existing rows.
  - Do NOT rely on a UNIQUE constraint existing on drugs.name for
    ON CONFLICT — instead fetch existing names, filter candidates in
    Python, and run a plain INSERT for what's left. This keeps us
    working even if that constraint isn't present on Neon, and avoids
    surprises from ON CONFLICT semantics.

All `drugs` / `drug_categories` tables already exist on Neon — this
module does not create tables.
"""

import json
import logging

import psycopg2
import psycopg2.extras

from config import POSTGRES_CONFIG, UNCATEGORIZED_CATEGORY_NAME, CANDIDATE_FILE

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)


def get_connection():
    return psycopg2.connect(**POSTGRES_CONFIG)


def get_or_create_uncategorized_category(cursor) -> int:
    """
    Looks up the "Uncategorized" category by name (case-insensitive).
    Creates it if missing. Returns its id.
    """
    cursor.execute(
        "SELECT id FROM drug_categories WHERE LOWER(name) = LOWER(%s)",
        (UNCATEGORIZED_CATEGORY_NAME,),
    )
    row = cursor.fetchone()
    if row:
        logger.info(f"Found existing '{UNCATEGORIZED_CATEGORY_NAME}' category (id={row[0]})")
        return row[0]

    cursor.execute(
        "INSERT INTO drug_categories (name, description, created_at) "
        "VALUES (%s, %s, NOW()) RETURNING id",
        (UNCATEGORIZED_CATEGORY_NAME, "Auto-created placeholder category for FDA-sourced drugs "
                                       "with no known category."),
    )
    new_id = cursor.fetchone()[0]
    logger.info(f"Created '{UNCATEGORIZED_CATEGORY_NAME}' category (id={new_id})")
    return new_id


def get_existing_names(cursor) -> set:
    """Returns the set of all existing drug names, lowercased+trimmed."""
    cursor.execute("SELECT name FROM drugs")
    return {row[0].strip().lower() for row in cursor.fetchall() if row[0]}


def filter_new_candidates(candidates: list, existing_names: set) -> list:
    """
    Filters the candidate list down to names not already present in
    the DB. Also de-duplicates within the candidate list itself
    (should already be deduped by extract_transform.py, but this is
    cheap insurance).
    """
    new_candidates = []
    seen = set()

    for candidate in candidates:
        key = candidate["name"].strip().lower()
        if key in existing_names or key in seen:
            continue
        seen.add(key)
        new_candidates.append(candidate)

    return new_candidates


def insert_new_drugs(cursor, new_candidates: list, category_id: int):
    """
    Plain batch INSERT (no ON CONFLICT) for rows already confirmed new.
    """
    if not new_candidates:
        logger.info("No new drugs to insert.")
        return

    rows = [
        (
            c["name"],
            c["active_substance"],
            c["dosage_form"],
            c["strength"],
            c["manufacturer"],
            c["description"],
            c["image_url"],
            category_id,
        )
        for c in new_candidates
    ]

    query = (
        "INSERT INTO drugs "
        "(name, active_substance, dosage_form, strength, manufacturer, "
        " description, image_url, category_id, created_at, updated_at) "
        "VALUES %s"
    )
    template = "(%s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())"

    psycopg2.extras.execute_values(cursor, query, rows, template=template, page_size=500)
    logger.info(f"Inserted {len(rows)} new drugs.")


def load():
    with open(CANDIDATE_FILE) as f:
        candidates = json.load(f)

    logger.info(f"Loaded {len(candidates)} candidate drugs from {CANDIDATE_FILE}")

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            category_id = get_or_create_uncategorized_category(cursor)
            existing_names = get_existing_names(cursor)
            logger.info(f"{len(existing_names)} drugs already exist in the database")

            new_candidates = filter_new_candidates(candidates, existing_names)
            logger.info(f"{len(new_candidates)} of {len(candidates)} candidates are genuinely new")

            insert_new_drugs(cursor, new_candidates, category_id)

        conn.commit()
        logger.info("Load complete. Committed.")
    except Exception:
        conn.rollback()
        logger.error("Load failed — rolled back.")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    load()

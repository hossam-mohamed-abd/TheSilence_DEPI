"""
push_to_postgres.py
--------------------
Reads final transformed tables from DuckDB
and pushes them to Neon PostgreSQL warehouse.

Execution order respects FK dependencies:
    1. drug_categories
    2. drugs
    3. drug_alternatives
    4. pharmacy_inventory
    5. drug_analytics
    6. price_history        (append only)
    7. availability_history (append only)

Dependencies:
    pip install duckdb psycopg2-binary pandas

CHANGES FROM PREVIOUS VERSION
──────────────────────────────────────────────────────────────
  POSTGRES_CONFIG : Replaced Azure PostgreSQL credentials with
                    Neon PostgreSQL credentials.
                    Added sslmode=require and options=endpoint=...
                    (both required by Neon's connection router)

  CORE_TABLES     : drug_categories conflict col: ["category_id"] → ["id"]
                    drugs           conflict col: ["drug_id"]      → ["id"]
                    drug_prices key → pharmacy_inventory
                    DuckDB source:  core_drug_prices → core_pharmacy_inventory
                    Conflict cols for pharmacy_inventory unchanged: ["drug_id", "pharmacy_id"]

  BUGFIX (post-deployment): CORE_TABLES entries now carry a third
  element, drop_cols, listing columns to exclude from the INSERT.
  pharmacy_inventory sets drop_cols=["id"] because its id column in
  PostgreSQL is BIGSERIAL — dbt's internal ROW_NUMBER()-generated id
  in core_pharmacy_inventory is recalculated from 1 every run, scoped
  only to that run's batch of pharmacy files, so forwarding it caused
  "duplicate key value violates unique constraint pharmacy_inventory_pkey"
  when two different runs assigned the same id to two different
  (drug_id, pharmacy_id) pairs. See create_tables.sql for full detail.
  upsert_rows() now accepts drop_cols and strips those columns from
  the DataFrame before building the INSERT statement.
"""

import duckdb
import psycopg2
import psycopg2.extras
import pandas as pd
import logging
from datetime import datetime

# ─────────────────────────────────────────────
# Logging setup
# ─────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────
DUCKDB_PATH = "/home/abram/Medical_System_Pipeline/dbt_architecture/drug_tracking.duckdb"

POSTGRES_CONFIG = {
    "host": "ep-spring-sound-atfc1f55-pooler.c-9.us-east-1.aws.neon.tech",
    "port": 5432,
    "database": "neondb",
    "user": "neondb_owner",
    "password": "npg_Gi2nkbKme4gx",
    "sslmode": "require",
    "options": "endpoint=ep-spring-sound-atfc1f55-pooler"  # ← add -pooler here
}

# ─────────────────────────────────────────────
# Table Definitions
# ─────────────────────────────────────────────
# Each entry: pg_table_name -> (duckdb_source, conflict_columns, drop_cols)
# conflict_columns = the UNIQUE/PRIMARY KEY columns used in ON CONFLICT (...)
# drop_cols         = columns to exclude from the INSERT entirely
#                     (e.g. an auto-generated PK that PostgreSQL must assign)
CORE_TABLES = {
    "drug_categories":   ("main_core.core_drug_categories",   ["id"],                      []),
    "drugs":             ("main_core.core_drugs",              ["id"],                      []),
    # "drug_alternatives": ("main_core.core_drug_alternatives",  ["drug_id", "alternative_drug_id"], []),

    # id is BIGSERIAL in PostgreSQL — never forward dbt's internal
    # ROW_NUMBER()-generated id here. That id is recalculated from 1
    # on every dbt run scoped only to the current batch of pharmacy
    # files, so two different runs can assign the same id to two
    # different (drug_id, pharmacy_id) pairs, causing a PK collision
    # on upsert. See create_tables.sql for the full explanation.
    "pharmacy_inventory":("main_core.core_pharmacy_inventory", ["drug_id", "pharmacy_id"],  ["id"]),

    "drug_analytics":    ("main_analytics.drug_analytics",     ["drug_id"],                 []),
}

HISTORY_TABLES = {
    "price_history":        "snapshots.price_history",
    "availability_history": "snapshots.availability_history",
}


# ─────────────────────────────────────────────
# Helper: Connect to PostgreSQL
# ─────────────────────────────────────────────
def get_pg_connection():
    return psycopg2.connect(**POSTGRES_CONFIG)


# ─────────────────────────────────────────────
# Helper: Read table from DuckDB
# ─────────────────────────────────────────────
def read_from_duckdb(duck_conn, duckdb_table: str) -> pd.DataFrame:
    logger.info(f"  Reading from DuckDB: {duckdb_table}")
    df = duck_conn.execute(f"SELECT * FROM {duckdb_table}").df()
    logger.info(f"  Rows fetched: {len(df)}")
    return df


# ─────────────────────────────────────────────
# Helper: Insert rows using psycopg2 directly
# Used by append_new_records (history tables only)
# ─────────────────────────────────────────────
def insert_rows(cursor, pg_table: str, df: pd.DataFrame):
    """
    Inserts all rows from a DataFrame into a PostgreSQL table
    using psycopg2 execute_values for batch performance.
    """
    if df.empty:
        logger.info(f"  No rows to insert for: {pg_table}")
        return

    columns = list(df.columns)
    col_str = ", ".join(columns)
    values = [tuple(row) for row in df.itertuples(index=False, name=None)]

    query = f"INSERT INTO {pg_table} ({col_str}) VALUES %s"
    psycopg2.extras.execute_values(cursor, query, values, page_size=500)
    logger.info(f"  Inserted {len(values)} rows into: {pg_table}")


# ─────────────────────────────────────────────
# Strategy 1: UPSERT (core tables)
# INSERT new rows; UPDATE existing rows on conflict.
# Old rows not present in the incoming data are preserved.
# ─────────────────────────────────────────────
def upsert_rows(df: pd.DataFrame, pg_table: str, conflict_cols: list, drop_cols: list = None):
    """
    Upserts all rows from a DataFrame into a PostgreSQL table.

    - Rows whose conflict_cols key already exists -> all other columns are updated.
    - Rows whose conflict_cols key is new         -> inserted fresh.
    - Rows already in PostgreSQL but absent here  -> left untouched.

    Uses INSERT ... ON CONFLICT (...) DO UPDATE SET ... so a single
    statement handles both cases efficiently with no TRUNCATE risk.

    drop_cols: columns to exclude from the INSERT entirely, e.g. an
    auto-generated PK (BIGSERIAL) that PostgreSQL must assign itself.
    Needed for pharmacy_inventory — see create_tables.sql for why its
    id column is BIGSERIAL and must never be supplied by dbt/DuckDB.
    """
    if df.empty:
        logger.info(f"  No rows to upsert for: {pg_table}")
        return

    if drop_cols:
        df = df.drop(columns=[c for c in drop_cols if c in df.columns])

    columns = list(df.columns)
    update_cols = [c for c in columns if c not in conflict_cols]

    col_str      = ", ".join(columns)
    conflict_str = ", ".join(conflict_cols)

    if update_cols:
        set_clause = ", ".join(f"{c} = EXCLUDED.{c}" for c in update_cols)
        query = (
            f"INSERT INTO {pg_table} ({col_str}) VALUES %s "
            f"ON CONFLICT ({conflict_str}) DO UPDATE SET {set_clause}"
        )
    else:
        # Every column is part of the PK — just skip duplicates
        query = (
            f"INSERT INTO {pg_table} ({col_str}) VALUES %s "
            f"ON CONFLICT ({conflict_str}) DO NOTHING"
        )

    values = [tuple(row) for row in df.itertuples(index=False, name=None)]

    conn = get_pg_connection()
    try:
        with conn.cursor() as cur:
            psycopg2.extras.execute_values(cur, query, values, page_size=500)
            logger.info(
                f"  Upserted {len(values)} rows into: {pg_table} "
                f"(conflict key: {conflict_str})"
            )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


# ─────────────────────────────────────────────
# Strategy 2: Append new records only (history tables)
# ─────────────────────────────────────────────
def append_new_records(
    df: pd.DataFrame,
    pg_table: str,
    timestamp_col: str
):
    conn = get_pg_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(f"SELECT MAX({timestamp_col}) FROM {pg_table}")
            latest_in_pg = cur.fetchone()[0]

        if latest_in_pg is None:
            new_records = df
            logger.info(f"  Table is empty, inserting all {len(df)} records")
        else:
            df[timestamp_col] = pd.to_datetime(df[timestamp_col])
            new_records = df[df[timestamp_col] > pd.to_datetime(latest_in_pg)]
            logger.info(
                f"  Latest in PostgreSQL: {latest_in_pg} | "
                f"New records to insert: {len(new_records)}"
            )

        if len(new_records) == 0:
            logger.info(f"  No new records to insert for: {pg_table}")
            conn.close()
            return

        with conn.cursor() as cur:
            insert_rows(cur, pg_table, new_records)
        conn.commit()

    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


# ─────────────────────────────────────────────
# MAIN FUNCTION
# ─────────────────────────────────────────────
def push_to_postgres():
    logger.info("=" * 60)
    logger.info("Starting push to PostgreSQL")
    logger.info(f"   Timestamp: {datetime.now()}")
    logger.info("=" * 60)

    # Connect to DuckDB
    logger.info("Connecting to DuckDB...")
    duck_conn = duckdb.connect(DUCKDB_PATH, read_only=True)
    logger.info("DuckDB connected")

    # Test PostgreSQL connection
    logger.info("Connecting to PostgreSQL...")
    test_conn = get_pg_connection()
    test_conn.close()
    logger.info("PostgreSQL connected")

    # ── Push Core Tables ──────────────────────
    logger.info("\n── Pushing Core Tables ──────────────────")
    for pg_table, (duck_table, conflict_cols, drop_cols) in CORE_TABLES.items():
        logger.info(f"\n> {pg_table}")
        try:
            df = read_from_duckdb(duck_conn, duck_table)
            upsert_rows(df, pg_table, conflict_cols, drop_cols=drop_cols)
            logger.info(f"  OK: {pg_table} done")
        except Exception as e:
            logger.error(f"  FAILED on {pg_table}: {e}")
            raise

    # ── Push History Tables ───────────────────
    logger.info("\n── Pushing History Tables ───────────────")

    logger.info(f"\n> price_history")
    try:
        df = read_from_duckdb(duck_conn, HISTORY_TABLES["price_history"])
        df = df[[
            "drug_id",
            "pharmacy_id",
            "price",
            "dbt_valid_from"
        ]].rename(columns={"dbt_valid_from": "recorded_at"})
        append_new_records(df, "price_history", "recorded_at")
        logger.info(f"  OK: price_history done")
    except Exception as e:
        logger.error(f"  FAILED on price_history: {e}")
        raise

    logger.info(f"\n> availability_history")
    try:
        df = read_from_duckdb(duck_conn, HISTORY_TABLES["availability_history"])
        df = df[[
            "drug_id",
            "pharmacy_id",
            "available",            # derived as (quantity > 0) in the snapshot
            "dbt_valid_from"
        ]].rename(columns={"dbt_valid_from": "checked_at"})
        append_new_records(df, "availability_history", "checked_at")
        logger.info(f"  OK: availability_history done")
    except Exception as e:
        logger.error(f"  FAILED on availability_history: {e}")
        raise

    duck_conn.close()

    logger.info("\n" + "=" * 60)
    logger.info("All tables pushed to PostgreSQL successfully")
    logger.info("=" * 60)


# ─────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────
if __name__ == "__main__":
    push_to_postgres()

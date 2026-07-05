"""
dags/drug_tracking_pipeline.py
--------------------------------
Main Airflow DAG for the Drug Tracking System pipeline.

Execution order:
    0. ingest_from_storage   → pull pharmacy files from Supabase Storage
                               into datalake/ (working copy) and
                               datalake_archive/<run_date>/ (permanent copy)
    1. normalize_csvs        → standardize pharmacy CSV column names,
                               then clean up datalake/ on success
    2. dbt_seed              → load normalized CSVs into DuckDB
    3. dbt_run               → build all staging, core, analytics models
    4. dbt_snapshot          → capture price & availability history
    5. push_to_postgres      → push final tables to Neon PostgreSQL

Schedule: every 12 hours at midnight and noon (FR-18: data refreshed daily)

CHANGES FROM PREVIOUS VERSION
──────────────────────────────────────────────────────────────
  NEW — Task 0: ingest_from_storage
    Files no longer originate from a manually populated datalake/ folder.
    The backend team now drops pharmacy uploads into Supabase Storage
    (bucket: medisearch-data-lake, folder: pharmacy_uploads/). This task
    downloads them locally before normalization runs. See
    storage_ingestion.py for full details.

  normalize_csvs_task:
    Pharmacy inventory CSV naming convention updated:
      drug_prices_pharmacy_<id>_<timestamp>.csv
        → pharmacy_inventory_pharmacy_<id>_<timestamp>.csv

    Fallback single-file name updated:
      drug_prices.csv → pharmacy_inventory.csv

    Merged seed output filename updated:
      seeds/drug_prices.csv → seeds/pharmacy_inventory.csv

    table_name arg to normalize_pharmacy_csv updated:
      "drug_prices" → "pharmacy_inventory"

    NEW — cleanup step added at the end of the task: datalake/ is now
    emptied after all files are successfully copied to seeds/. This only
    runs if normalization completes without raising — a failed run leaves
    datalake/ intact for debugging/retry. datalake_archive/ is never
    touched by this cleanup; it is the permanent record.

  push_to_postgres_task:
    Docstring updated: Azure PostgreSQL → Neon PostgreSQL
    (connection config change is in push_to_postgres.py)
"""

from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# ─────────────────────────────────────────────
# Project paths
# ─────────────────────────────────────────────
PROJECT_ROOT    = "/home/abram/Medical_System_Pipeline"
DBT_PROJECT_DIR = f"{PROJECT_ROOT}/dbt_architecture/drug_tracking"
DBT_VENV        = f"{PROJECT_ROOT}/dbt_env/bin/activate"
DATALAKE_DIR    = f"{PROJECT_ROOT}/datalake"
SEEDS_DIR       = f"{DBT_PROJECT_DIR}/seeds"

# Add project root to path so Airflow can import our scripts
sys.path.insert(0, PROJECT_ROOT)


# ─────────────────────────────────────────────
# Default DAG arguments
# ─────────────────────────────────────────────
default_args = {
    "owner":            "abram",
    "retries":          2,                        # retry twice on failure
    "retry_delay":      timedelta(minutes=1),     # wait 1 min before retry
    "email_on_failure": False,
    "email_on_retry":   False,
}


# ─────────────────────────────────────────────
# Task 0 — Ingest from Supabase Storage
# Pulls pharmacy-uploaded files from the medisearch-data-lake bucket
# into datalake/ (working copy) and datalake_archive/<run_date>/
# (permanent copy), then deletes them from storage.
# ─────────────────────────────────────────────
def ingest_from_storage_task():
    """
    Calls storage_ingestion.py to pull all pending pharmacy files from
    Supabase Storage. Raises if any file fails to ingest, so Airflow's
    retry mechanism can pick it up — files that failed are left in
    storage (not deleted) and will be retried on the next attempt.
    """
    from storage_ingestion import ingest_from_storage

    summary = ingest_from_storage()

    if summary["failed"]:
        raise RuntimeError(
            f"{len(summary['failed'])} file(s) failed to ingest from "
            f"storage: {summary['failed']}"
        )


# ─────────────────────────────────────────────
# Task 1 — Normalize CSVs
# Runs column_normalizer.py on all CSV files in datalake/
# Saves normalized CSVs to seeds/ folder
# ─────────────────────────────────────────────
def normalize_csvs_task():
    """
    Scans the datalake folder for CSV files,
    normalizes their column names using column_normalizer.py,
    and saves the cleaned versions to the seeds/ folder.

    Two categories of files are handled:

    Structured CSVs (exact filename match) — maintained by the data team,
    copied directly to seeds/ without normalization:
        drugs.csv
        drug_categories.csv
        drug_alternatives.csv

    Pharmacy inventory CSVs (pattern match) — uploaded by individual
    pharmacies, normalized via column_normalizer.py, then merged and
    deduplicated into a single seed file:
        Naming convention: pharmacy_inventory_pharmacy_<id>_<timestamp>.csv
        Fallback single file: pharmacy_inventory.csv
        Merged output:        seeds/pharmacy_inventory.csv
        Deduplication key:    most recent record per (pharmacy_id, name) pair

    Any file that does not match either pattern is skipped with a warning.
    """
    from column_normalizer import normalize_pharmacy_csv
    import shutil
    import pandas as pd

    # Exact match → structured CSVs maintained by the data team
    EXACT_FILES = {
        "drugs.csv":              "drugs",
        "drug_categories.csv":    "drug_categories",
        "drug_alternatives.csv":  "drug_alternatives",
    }

    # Check datalake exists
    if not os.path.exists(DATALAKE_DIR):
        raise FileNotFoundError(f"Datalake directory not found: {DATALAKE_DIR}")

    csv_files = [f for f in os.listdir(DATALAKE_DIR) if f.endswith(".csv")]

    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in datalake: {DATALAKE_DIR}")

    # ── Handle structured CSVs (exact match) ──────────────────
    for filename, table_name in EXACT_FILES.items():
        if filename not in csv_files:
            print(f"⚠️  Expected file not found in datalake: {filename}")
            continue

        filepath = os.path.join(DATALAKE_DIR, filename)
        output_path = os.path.join(SEEDS_DIR, filename)
        shutil.copy(filepath, output_path)
        print(f"✅ Copied {filename} to seeds/")

    # ── Handle pharmacy inventory CSVs (pattern match) ────────
    # Matches: pharmacy_inventory.csv
    #       OR pharmacy_inventory_pharmacy_<id>_<timestamp>.csv
    pharmacy_files = [
        f for f in csv_files
        if f == "pharmacy_inventory.csv" or f.startswith("pharmacy_inventory_pharmacy_")
    ]

    if not pharmacy_files:
        print("⚠️  No pharmacy inventory CSV files found in datalake")
    else:
        all_dfs = []

        for filename in pharmacy_files:
            filepath = os.path.join(DATALAKE_DIR, filename)
            print(f"▶ Normalizing: {filename}")

            clean_df, report = normalize_pharmacy_csv(
                filepath=filepath,
                table_name="pharmacy_inventory"
            )

            if report["status"] == "INCOMPLETE":
                print(f"⚠️  Missing columns in {filename}: {report['missing']}")
                continue

            all_dfs.append(clean_df)
            print(f"✅ Normalized: {filename} ({len(clean_df)} rows)")

        if all_dfs:
            # Merge all pharmacy uploads into one seed file
            merged_df = pd.concat(all_dfs, ignore_index=True)

            # Deduplicate — keep most recent record per pharmacy/drug pair
            merged_df["last_updated"] = pd.to_datetime(merged_df["last_updated"])
            merged_df = (
                merged_df
                .sort_values("last_updated", ascending=False)
                .drop_duplicates(subset=["pharmacy_id", "drug_id"], keep="first")
                .reset_index(drop=True)
            )

            output_path = os.path.join(SEEDS_DIR, "pharmacy_inventory.csv")
            merged_df.to_csv(output_path, index=False)
            print(
                f"✅ Merged {len(pharmacy_files)} pharmacy file(s) → "
                f"seeds/pharmacy_inventory.csv ({len(merged_df)} rows)"
            )
        else:
            print("❌ No valid pharmacy inventory files to process")

    # ── Skip any unrecognized files ────────────────────────────
    recognized = (
        set(EXACT_FILES.keys()) |
        {
            f for f in csv_files
            if f == "pharmacy_inventory.csv"
            or f.startswith("pharmacy_inventory_pharmacy_")
        }
    )
    unrecognized = [f for f in csv_files if f not in recognized]
    for f in unrecognized:
        print(f"⚠️  Skipping unrecognized file: {f}")

    print("✅ All CSV files processed successfully")

    # ── Clean up datalake/ ──────────────────────────────────────
    # Only reached if the function completed without raising —
    # a failure anywhere above leaves datalake/ intact for retry/debugging.
    #
    # Only files we actually recognized and processed are removed.
    # Unrecognized files are left in place so nothing is silently lost
    # and the data team can investigate them on the next run.
    #
    # datalake_archive/ is never touched here — it already holds a
    # permanent copy of every file written by ingest_from_storage_task,
    # regardless of whether normalization later succeeded or failed.
    removed = 0
    for filename in recognized:
        filepath = os.path.join(DATALAKE_DIR, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            removed += 1

    print(f"🧹 Cleaned up {removed} processed file(s) from datalake/")


# ─────────────────────────────────────────────
# Task 5 — Push to PostgreSQL
# Calls push_to_postgres.py
# ─────────────────────────────────────────────
def push_to_postgres_task():
    """
    Reads final tables from DuckDB and pushes them to Neon PostgreSQL.
    Connection config (host, credentials, sslmode, endpoint) is defined
    in push_to_postgres.py.
    """
    from push_to_postgres import push_to_postgres
    push_to_postgres()


# ─────────────────────────────────────────────
# DAG Definition
# ─────────────────────────────────────────────
with DAG(
    dag_id              = "drug_tracking_pipeline",
    description         = "Drug Tracking System pipeline — runs every 12 hours",
    default_args        = default_args,
    start_date          = datetime(2026, 4, 25),
    schedule            = "0 0,12 * * *",     # midnight and noon every day
    catchup             = False,              # don't backfill missed runs
    tags                = ["drug_tracking", "medical", "depi"],
) as dag:

    # ── Task 0: Ingest from Supabase Storage ──
    # Pulls pharmacy files into datalake/ (working copy) and
    # datalake_archive/<run_date>/ (permanent copy), then removes
    # them from the medisearch-data-lake bucket.
    ingest_from_storage = PythonOperator(
        task_id         = "ingest_from_storage",
        python_callable = ingest_from_storage_task,
    )

    # ── Task 1: Normalize CSVs ────────────────
    normalize_csvs = PythonOperator(
        task_id         = "normalize_csvs",
        python_callable = normalize_csvs_task,
    )

    # ── Task 2: dbt Seed ─────────────────────
    # Loads all CSVs from seeds/ into DuckDB
    dbt_seed = BashOperator(
        task_id         = "dbt_seed",
        bash_command    = f"""
            source {DBT_VENV} &&
            cd {DBT_PROJECT_DIR} &&
            dbt seed --profiles-dir ~/.dbt
        """,
    )

    # ── Task 3: dbt Run ──────────────────────
    # Builds all staging, core, and analytics models in DuckDB
    dbt_run = BashOperator(
        task_id         = "dbt_run",
        bash_command    = f"""
            source {DBT_VENV} &&
            cd {DBT_PROJECT_DIR} &&
            dbt run --profiles-dir ~/.dbt
        """,
    )

    # ── Task 4: dbt Snapshot ─────────────────
    # Runs price_history and availability_history snapshots
    dbt_snapshot = BashOperator(
        task_id         = "dbt_snapshot",
        bash_command    = f"""
            source {DBT_VENV} &&
            cd {DBT_PROJECT_DIR} &&
            dbt snapshot --profiles-dir ~/.dbt
        """,
    )

    # ── Task 5: Push to PostgreSQL ────────────
    # Upserts core/analytics tables and appends history tables to Neon
    push_to_postgres = PythonOperator(
        task_id         = "push_to_postgres",
        python_callable = push_to_postgres_task,
    )

    # ── Task Dependencies (execution order) ───
    ingest_from_storage >> normalize_csvs >> dbt_seed >> dbt_run >> dbt_snapshot >> push_to_postgres

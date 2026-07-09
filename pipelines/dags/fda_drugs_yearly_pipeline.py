"""
dags/fda_drugs_yearly_pipeline.py
------------------------------------
Yearly pipeline that discovers, samples, transforms, and incrementally
loads openFDA drug/event data into the `drugs` table (Neon PostgreSQL).

Execution order:
    1. discover_task          -> find all quarters/parts for the current
                                  year via openFDA's download.json index,
                                  select a small sample (<= MAX_SAMPLE_MB)
    2. extract_transform_task -> stream-download only the sampled files,
                                  map fields to the `drugs` schema, dedupe
    3. load_task               -> insert-only load of genuinely new drugs

Schedule: once a year, Jan 2nd at midnight.

NOTE: This is a proof-of-concept pipeline (graduation project scope) —
see fda_drugs_pipeline/config.py:MAX_SAMPLE_MB for why only a small
sample of the year's data is processed rather than the full dataset.
"""

import sys
from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

# ─────────────────────────────────────────────
# Project paths
# ─────────────────────────────────────────────
PROJECT_ROOT = "/home/abram/Medical_System_Pipeline"
FDA_PIPELINE_DIR = f"{PROJECT_ROOT}/fda_drugs_pipeline"

# Add the fda_drugs_pipeline folder to path so Airflow can import
# discover.py / extract_transform.py / load.py / config.py directly
sys.path.insert(0, FDA_PIPELINE_DIR)


# ─────────────────────────────────────────────
# Default DAG arguments
# ─────────────────────────────────────────────
default_args = {
    "owner":            "abram",
    "retries":          2,
    "retry_delay":      timedelta(minutes=1),
    "email_on_failure": False,
    "email_on_retry":   False,
}


# ─────────────────────────────────────────────
# Task callables
# ─────────────────────────────────────────────
def discover_task(**context):
    from discover import discover
    result = discover()
    # Push just the small summary to XCom; the full partition lists
    # already live on disk at config.DISCOVERY_FILE for the next task.
    context["ti"].xcom_push(key="year", value=result["year"])
    context["ti"].xcom_push(key="total_partitions_found", value=result["total_partitions_found"])
    context["ti"].xcom_push(key="sampled_count", value=len(result["sampled_partitions"]))


def extract_transform_task(**context):
    import json
    from config import DISCOVERY_FILE
    from extract_transform import extract_transform

    with open(DISCOVERY_FILE) as f:
        discovery_result = json.load(f)

    candidates = extract_transform(discovery_result)
    context["ti"].xcom_push(key="candidate_count", value=len(candidates))


def load_task(**context):
    from load import load
    load()


# ─────────────────────────────────────────────
# DAG Definition
# ─────────────────────────────────────────────
with DAG(
    dag_id              = "fda_drugs_yearly_pipeline",
    description         = "Yearly discovery + incremental load of openFDA drug data (POC sample)",
    default_args        = default_args,
    start_date          = datetime(2026, 1, 1),
    schedule            = "0 0 2 1 *",   # once a year: Jan 2nd, midnight
    catchup             = False,
    tags                = ["drug_tracking", "medical", "depi", "fda", "yearly"],
) as dag:

    discover = PythonOperator(
        task_id         = "discover",
        python_callable = discover_task,
    )

    extract_transform = PythonOperator(
        task_id         = "extract_transform",
        python_callable = extract_transform_task,
    )

    load = PythonOperator(
        task_id         = "load",
        python_callable = load_task,
    )

    discover >> extract_transform >> load

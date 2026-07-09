"""
fda_drugs_pipeline/config.py
-----------------------------
Shared configuration for the yearly FDA drug-discovery pipeline.

Connection settings follow the same pattern as push_to_postgres.py
(plain constants in-file, psycopg2-style config dict) rather than
introducing a new secrets pattern for this project.
"""

import os

# ─────────────────────────────────────────────
# PostgreSQL (Neon) connection
# Parsed from:
# postgresql://neondb_owner:npg_Gi2nkbKme4gx@ep-spring-sound-atfc1f55-pooler.c-9.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
# ─────────────────────────────────────────────
POSTGRES_CONFIG = {
    "host":     "ep-spring-sound-atfc1f55-pooler.c-9.us-east-1.aws.neon.tech",
    "port":     5432,
    "database": "neondb",
    "user":     "neondb_owner",
    "password": "npg_Gi2nkbKme4gx",
    "sslmode":  "require",
    "options": "endpoint=ep-spring-sound-atfc1f55-pooler"
}


# ─────────────────────────────────────────────
# openFDA discovery
# ─────────────────────────────────────────────
DOWNLOAD_INDEX_URL = "https://api.fda.gov/download.json"

# Path in the download.json tree: results -> drug -> event -> partitions
ENDPOINT_DOMAIN    = "drug"
ENDPOINT_SUBTYPE   = "event"

# ─────────────────────────────────────────────
# Proof-of-concept sampling cap
# -----------------------------------------------
# This is NOT a production setting. The graduation-project scope only
# needs to prove the pipeline works end-to-end, not ingest a full year
# of openFDA data (which is tens of GB and would blow through our
# Neon connection/query limits). We cap how much raw data we pull
# down and process to this many megabytes, even though `discover.py`
# still reports the FULL list of quarters/files that genuinely exist
# for the year.
# ─────────────────────────────────────────────
MAX_SAMPLE_MB = 150

# ─────────────────────────────────────────────
# Business rules
# ─────────────────────────────────────────────
UNCATEGORIZED_CATEGORY_NAME = "Uncategorized"

# ─────────────────────────────────────────────
# Paths
# ─────────────────────────────────────────────
PROJECT_ROOT = "/home/abram/Medical_System_Pipeline"
PIPELINE_DIR = os.path.join(PROJECT_ROOT, "fda_drugs_pipeline")
WORK_DIR     = os.path.join(PIPELINE_DIR, "work")

DISCOVERY_FILE  = os.path.join(WORK_DIR, "discovered_partitions.json")
CANDIDATE_FILE  = os.path.join(WORK_DIR, "candidate_drugs.json")

os.makedirs(WORK_DIR, exist_ok=True)

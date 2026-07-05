"""
storage_ingestion.py
---------------------
Pulls pharmacy-uploaded files from Supabase Storage (the middleware
data lake the backend team writes to) into the local pipeline
environment, ready for column_normalizer.py to process.

Responsibilities:
    1. Connect to Supabase Storage using credentials from environment
       variables (never hardcoded).
    2. List all files currently sitting in the pharmacy_uploads/ folder
       of the medisearch-data-lake bucket.
    3. For each file:
         a. Download it into the local datalake/ folder
            (this is the working folder normalize_csvs_task reads from —
            unchanged from before).
         b. Save a second copy into datalake_archive/<run_date>/
            (a permanent historical record, organized by the date the
            pipeline run processed the file).
         c. Delete the file from Supabase Storage, since the backend
            team's bucket is a drop-off point, not permanent storage —
            our local datalake_archive/ is now the permanent record.
    4. Log a summary of how many files were pulled and any failures.

IMPORTANT — env vars required:
    SUPABASE_URL
    SUPABASE_KEY   (service_role key — backend/pipeline only, never
                    exposed to frontend code)

Dependencies:
    pip install supabase
"""

import os
import logging
from datetime import datetime

from supabase import create_client

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
BUCKET_NAME       = "medisearch-data-lake"
STORAGE_FOLDER    = "pharmacy_uploads"

PROJECT_ROOT      = "/home/abram/Medical_System_Pipeline"
DATALAKE_DIR      = f"{PROJECT_ROOT}/datalake"
DATALAKE_ARCHIVE  = f"{PROJECT_ROOT}/datalake_archive"


# ─────────────────────────────────────────────
# Helper: Build Supabase client
# ─────────────────────────────────────────────
def get_supabase_client():
    """
    Creates a Supabase client using credentials from environment variables.
    Raises a clear error if either variable is missing, rather than
    failing with an opaque connection error later.
    """
    # supabase_url = os.environ.get("SUPABASE_URL")
    # supabase_key = os.environ.get("SUPABASE_KEY")

    supabase_url = "https://qthxwtthzikwmmcnlxip.supabase.co"
    supabase_key = "sb_secret_GFuU_tmElpo_-yYJRgtyCQ_euYeapkL"


    if not supabase_url or not supabase_key:
        raise EnvironmentError(
            "Missing SUPABASE_URL or SUPABASE_KEY environment variables. "
            "Set them before running the pipeline (e.g. in the systemd "
            "unit file's Environment= directives, or in airflow_env's "
            "activation)."
        )

    return create_client(supabase_url, supabase_key)


# ─────────────────────────────────────────────
# MAIN FUNCTION
# ─────────────────────────────────────────────
def ingest_from_storage():
    """
    Full ingestion pipeline:
        Supabase Storage → datalake/ (working copy)
                         → datalake_archive/<run_date>/ (permanent copy)
                         → deleted from Supabase Storage

    Returns a summary dict for logging/debugging purposes.
    """
    logger.info("=" * 60)
    logger.info("Starting ingestion from Supabase Storage")
    logger.info(f"   Timestamp: {datetime.now()}")
    logger.info("=" * 60)

    supabase = get_supabase_client()

    # Run-date subfolder for the archive — grouped by when the
    # pipeline processed the file, not when the pharmacy uploaded it.
    run_date = datetime.now().strftime("%Y-%m-%d")
    archive_dir = os.path.join(DATALAKE_ARCHIVE, run_date)

    os.makedirs(DATALAKE_DIR, exist_ok=True)
    os.makedirs(archive_dir, exist_ok=True)

    # ── List files in the bucket folder ───────────────────────
    logger.info(f"Listing files in {BUCKET_NAME}/{STORAGE_FOLDER}...")
    entries = supabase.storage.from_(BUCKET_NAME).list(STORAGE_FOLDER)

    # Supabase list() returns folder placeholders too in some cases;
    # filter down to actual files (entries with a name and no children).
    files = [e for e in entries if e.get("name")]

    if not files:
        logger.info("No files found in pharmacy_uploads/. Nothing to ingest.")
        return {
            "downloaded": 0,
            "archived":   0,
            "deleted":    0,
            "failed":     [],
        }

    logger.info(f"Found {len(files)} file(s) to ingest")

    downloaded = 0
    archived   = 0
    deleted    = 0
    failed     = []

    for entry in files:
        filename = entry["name"]
        storage_path = f"{STORAGE_FOLDER}/{filename}"

        try:
            logger.info(f"▶ Downloading: {storage_path}")

            # Download file bytes from Supabase Storage
            file_bytes = supabase.storage.from_(BUCKET_NAME).download(storage_path)

            # ── Write working copy to datalake/ ───────────────
            local_path = os.path.join(DATALAKE_DIR, filename)
            with open(local_path, "wb") as f:
                f.write(file_bytes)
            downloaded += 1
            logger.info(f"  ✅ Saved working copy: {local_path}")

            # ── Write permanent copy to datalake_archive/<run_date>/ ──
            archive_path = os.path.join(archive_dir, filename)
            with open(archive_path, "wb") as f:
                f.write(file_bytes)
            archived += 1
            logger.info(f"  ✅ Saved archive copy: {archive_path}")

            # ── Delete from Supabase Storage ──────────────────
            # Only delete after both local copies are confirmed written,
            # so a mid-download failure never results in data loss.
            supabase.storage.from_(BUCKET_NAME).remove([storage_path])
            deleted += 1
            logger.info(f"  ✅ Removed from storage: {storage_path}")

        except Exception as e:
            logger.error(f"  ❌ Failed to ingest {filename}: {e}")
            failed.append({"filename": filename, "error": str(e)})
            # Do not delete from storage if anything failed —
            # leave it there so the next run retries it.
            continue

    logger.info("=" * 60)
    logger.info(
        f"Ingestion complete | Downloaded: {downloaded} | "
        f"Archived: {archived} | Deleted from storage: {deleted} | "
        f"Failed: {len(failed)}"
    )
    if failed:
        logger.warning(f"Failed files (left in storage for retry): {failed}")
    logger.info("=" * 60)

    return {
        "downloaded": downloaded,
        "archived":   archived,
        "deleted":    deleted,
        "failed":     failed,
    }


# ─────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────
if __name__ == "__main__":
    ingest_from_storage()

"""
fda_drugs_pipeline/discover.py
--------------------------------
Discovers every openFDA drug/event file available for the CURRENT year,
with nothing hardcoded (no year, no quarter names, no file-count guesses).

openFDA publishes a single machine-readable index at:
    https://api.fda.gov/download.json

It lists, per endpoint, every downloadable partition with its direct
file URL, record count, and size in MB — e.g.:

    results.drug.event.partitions = [
        {
            "size_mb": "12.34",
            "records": 45000,
            "display_name": "2026 q1 (all)",
            "file": "https://download.open.fda.gov/drug/event/2026q1/drug-event-0001-of-0030.json.zip"
        },
        ...
    ]

This is far more robust than guessing quarter folder names or probing
sequential part numbers by HTTP status code, which is what the original
notebook did.

Because this is a graduation-project proof of concept (not a production
ingestion job), we still discover and log the FULL list of files that
genuinely exist for the year, but only SELECT a small sample of them
(capped at config.MAX_SAMPLE_MB) to actually download and process in
extract_transform.py. This keeps us well within our Neon connection/
query limits.
"""

import json
import logging

import requests

from config import DOWNLOAD_INDEX_URL, ENDPOINT_DOMAIN, ENDPOINT_SUBTYPE, MAX_SAMPLE_MB, DISCOVERY_FILE
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)


def get_current_year() -> int:
    """Returns the current year at runtime. Never hardcoded."""
    return datetime.now().year


def fetch_download_index() -> dict:
    """
    Fetches openFDA's full download index (a few hundred KB of JSON
    metadata — not drug data itself).
    """
    logger.info(f"Fetching openFDA download index: {DOWNLOAD_INDEX_URL}")
    response = requests.get(DOWNLOAD_INDEX_URL, timeout=30)
    response.raise_for_status()
    return response.json()


def find_year_partitions(index_json: dict, year: int) -> list:
    """
    Walks results[ENDPOINT_DOMAIN][ENDPOINT_SUBTYPE].partitions and
    returns every partition whose display_name belongs to `year`
    (display_name looks like "2026 q1 (all)").
    """
    try:
        partitions = index_json["results"][ENDPOINT_DOMAIN][ENDPOINT_SUBTYPE]["partitions"]
    except KeyError as e:
        raise RuntimeError(
            f"Unexpected download.json shape — missing key {e}. "
            f"openFDA may have changed their index format."
        )

    year_prefix = str(year)
    matches = [p for p in partitions if p.get("display_name", "").startswith(year_prefix)]

    logger.info(f"Discovered {len(matches)} total partitions for year {year} "
                f"(out of {len(partitions)} partitions across all years)")

    return matches


def select_sample(partitions: list, max_sample_mb: float) -> list:
    """
    Walks the full, ordered list of discovered partitions and greedily
    accumulates them into a sample selection until adding the next
    partition would exceed `max_sample_mb`. Stops there.

    This is a POC-scope cap only — see config.MAX_SAMPLE_MB docstring.
    """
    selected = []
    cumulative_mb = 0.0

    for partition in partitions:
        size_mb = float(partition.get("size_mb", 0))

        if size_mb > max_sample_mb:
            logger.warning(
                f"Partition {partition.get('display_name')} is {size_mb:.2f} MB, "
                f"which exceeds the sample cap of {max_sample_mb} MB. "
                "It will be skipped."
            )
            continue

        if cumulative_mb + size_mb > max_sample_mb:
            # Stop as soon as the next file would breach the cap.
            # (We don't try to squeeze in a smaller later file out of
            # order — sampling in discovery order is simpler and
            # reproducible.)
            break

        selected.append(partition)
        cumulative_mb += size_mb

    logger.info(
        f"Selected {len(selected)} of {len(partitions)} discovered partitions "
        f"as the sample (~{cumulative_mb:.2f} MB, cap={max_sample_mb} MB)"
    )

    if not selected and partitions:
        logger.warning(
            "No partitions fit under the sample cap (first file may already "
            "exceed MAX_SAMPLE_MB) — the sample will be empty this run."
        )

    return selected


def discover() -> dict:
    """
    Full discovery step. Returns and persists a dict with:
      - year
      - total_partitions_found  (everything that genuinely exists)
      - all_partitions          (full list, for visibility/logging)
      - sampled_partitions      (the capped subset extract_transform.py will use)
    """
    year = get_current_year()
    index_json = fetch_download_index()
    all_partitions = find_year_partitions(index_json, year)
    sampled_partitions = select_sample(all_partitions, MAX_SAMPLE_MB)

    result = {
        "year": year,
        "total_partitions_found": len(all_partitions),
        "all_partitions": all_partitions,
        "sampled_partitions": sampled_partitions,
    }

    with open(DISCOVERY_FILE, "w") as f:
        json.dump(result, f, indent=2)

    logger.info(f"Discovery complete. Wrote {DISCOVERY_FILE}")
    return result


if __name__ == "__main__":
    discover()

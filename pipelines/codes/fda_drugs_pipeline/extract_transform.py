"""
fda_drugs_pipeline/extract_transform.py
-----------------------------------------
Downloads only the sampled partitions selected by discover.py, entirely
in memory (no raw zip/JSON ever touches disk), extracts every drug
mention, maps it onto the new `drugs` table schema, and deduplicates
by name (case-insensitive) across the whole sample.

Field mapping (drug/event -> drugs), agreed with the project owner:

    drugs.name              <- openfda.generic_name[0]
                                 -> openfda.brand_name[0]
                                 -> medicinalproduct   (always present)
    drugs.active_substance  <- activesubstance.activesubstancename
                                 -> openfda.substance_name[0]
    drugs.dosage_form       <- drugdosageform            (drug-level field)
    drugs.manufacturer      <- openfda.manufacturer_name[0]
    drugs.strength          <- NULL, always.
                                 openFDA drug/event only carries a
                                 PER-REPORT administered dose
                                 (drugstructuredosagenumb/unit), not a
                                 stable per-product strength — storing
                                 it would be misleading. Not a temporary
                                 gap; a real limitation of this endpoint.
    drugs.description       <- NULL (no such field in openFDA drug data)
    drugs.image_url         <- NULL (openFDA has no product image field)
    drugs.category_id       <- resolved separately in load.py to the
                                 "Uncategorized" category

Everything else (dose text, reactions, patient info, etc.) is out of
scope for the `drugs` master table and is discarded.
"""

import io
import json
import logging
import zipfile

import requests

from config import CANDIDATE_FILE

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)


def _first_or_none(value):
    """openfda fields are lists; return the first element or None."""
    if isinstance(value, list) and value:
        return value[0]
    return None


def download_partition_in_memory(file_url: str) -> bytes:
    """
    Streams a single partition zip into memory and returns its raw bytes.
    Never writes the zip to disk.
    """
    logger.info(f"  Downloading (in-memory): {file_url}")
    response = requests.get(file_url, stream=True, timeout=180)
    response.raise_for_status()
    return response.content


def extract_json_records(zip_bytes: bytes) -> list:
    """
    Opens the zip from memory, reads the single inner .json file,
    and returns its `results` list. Never extracts to disk.
    """
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
        json_names = [n for n in zf.namelist() if n.endswith(".json")]
        if not json_names:
            raise ValueError("No .json file found inside partition zip")

        with zf.open(json_names[0]) as f:
            payload = json.load(f)

    return payload.get("results", [])


def map_drug_entry(drug_entry: dict) -> dict | None:
    """
    Maps a single patient.drug[] entry to the drugs table schema.
    Returns None if we can't even determine a name (shouldn't normally
    happen since medicinalproduct is effectively always present).
    """
    openfda = drug_entry.get("openfda", {}) or {}

    name = (
        _first_or_none(openfda.get("generic_name"))
        or _first_or_none(openfda.get("brand_name"))
        or drug_entry.get("medicinalproduct")
    )

    if not name or not str(name).strip():
        return None

    active_substance = (
        (drug_entry.get("activesubstance") or {}).get("activesubstancename")
        or _first_or_none(openfda.get("substance_name"))
    )

    dosage_form = drug_entry.get("drugdosageform")
    manufacturer = _first_or_none(openfda.get("manufacturer_name"))

    return {
        "name": str(name).strip(),
        "active_substance": active_substance.strip() if active_substance else None,
        "dosage_form": dosage_form.strip() if dosage_form else None,
        "strength": None,       # see module docstring — permanent, not TODO
        "manufacturer": manufacturer.strip() if manufacturer else None,
        "description": None,    # not present in openFDA drug data
        "image_url": None,      # not present in openFDA drug data
    }


def process_partitions(sampled_partitions: list) -> list:
    """
    Downloads + parses + maps every sampled partition, deduplicating
    candidate drug rows by lower(name) across the entire sample
    (first occurrence wins).

    Returns a list of unique candidate drug dicts.
    """
    seen_names = set()
    candidates = []

    for i, partition in enumerate(sampled_partitions, start=1):
        file_url = partition["file"]
        logger.info(f"[{i}/{len(sampled_partitions)}] Processing partition: {partition.get('display_name')}")

        try:
            zip_bytes = download_partition_in_memory(file_url)
            records = extract_json_records(zip_bytes)
        except Exception as e:
            logger.error(f"  Failed to download/parse {file_url}: {e} — skipping this partition")
            continue

        logger.info(f"  Parsed {len(records)} event records")

        new_in_this_partition = 0
        for record in records:
            drug_entries = (record.get("patient") or {}).get("drug") or []
            for drug_entry in drug_entries:
                mapped = map_drug_entry(drug_entry)
                if mapped is None:
                    continue

                key = mapped["name"].lower()
                if key in seen_names:
                    continue

                seen_names.add(key)
                candidates.append(mapped)
                new_in_this_partition += 1

        logger.info(f"  +{new_in_this_partition} new unique drug names "
                    f"(running total: {len(candidates)})")

    return candidates


def extract_transform(discovery_result: dict) -> list:
    """
    Entry point used by the DAG. Takes the dict produced by discover.discover()
    (or loaded from DISCOVERY_FILE), processes the sampled partitions, writes
    the deduplicated candidate list to CANDIDATE_FILE, and returns it.
    """
    sampled_partitions = discovery_result.get("sampled_partitions", [])

    if not sampled_partitions:
        logger.warning("No sampled partitions to process — writing empty candidate file")
        candidates = []
    else:
        candidates = process_partitions(sampled_partitions)

    with open(CANDIDATE_FILE, "w") as f:
        json.dump(candidates, f, indent=2)

    logger.info(f"Extract/transform complete. {len(candidates)} unique candidate drugs "
                f"written to {CANDIDATE_FILE}")

    return candidates


if __name__ == "__main__":
    from config import DISCOVERY_FILE

    with open(DISCOVERY_FILE) as f:
        discovery_result = json.load(f)

    extract_transform(discovery_result)

"""
Entry point. Dimensions load first, always -- fact rows FK-reference them,
so loading facts before dims risks FK violations against keys that don't
exist yet
"""
import sys
import logging
from dotenv import load_dotenv
load_dotenv()

import config
from db import get_oltp_engine, get_dw_engine
from dims import load_all_dimensions
from facts import load_all_facts

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("etl")


def main():
    log.info("Starting ETL run for %s (search_log mode: %s)", config.SNAPSHOT_DATE, config.SEARCH_LOG_MODE)

    oltp_engine = get_oltp_engine()
    dw_engine = get_dw_engine()

    log.info("Loading dimensions...")
    dim_counts = load_all_dimensions(oltp_engine, dw_engine)
    for name, count in dim_counts.items():
        log.info("  %s: %d rows upserted", name, count)

    log.info("Loading facts...")
    fact_counts = load_all_facts(oltp_engine, dw_engine)
    for name, count in fact_counts.items():
        log.info("  %s: %d rows loaded", name, count)

    log.info("ETL run complete.")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        log.exception("ETL run failed")
        sys.exit(1)  # non-zero exit so GitHub Actions marks the run as failed

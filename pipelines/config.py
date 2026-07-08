"""
Required env vars:
  OLTP_DATABASE_URL   e.g. mssql+pyodbc://user:pass@host/db?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes
  DW_DATABASE_URL     e.g. postgresql+psycopg2://user:pass@ep-xxxx.neon.tech/dbname?sslmode=require

"""
import os
from datetime import datetime, timezone

OLTP_DATABASE_URL = os.environ["OLTP_DATABASE_URL"]
DW_DATABASE_URL = os.environ["DW_DATABASE_URL"]

SEARCH_LOG_MODE = os.environ.get("SEARCH_LOG_MODE", "single").lower()
if SEARCH_LOG_MODE not in ("single", "multi"):
    raise ValueError(f"SEARCH_LOG_MODE must be 'single' or 'multi', got {SEARCH_LOG_MODE!r}")

_snapshot_override = os.environ.get("SNAPSHOT_DATE")
if _snapshot_override:
    SNAPSHOT_DATE = datetime.strptime(_snapshot_override, "%Y-%m-%d").date()
else:
    SNAPSHOT_DATE = datetime.now(timezone.utc).date()

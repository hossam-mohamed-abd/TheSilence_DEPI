
from sqlalchemy import create_engine
import config


def get_oltp_engine():
    return create_engine(config.OLTP_DATABASE_URL, pool_pre_ping=True)


def get_dw_engine():
    """pool_pre_ping forces a liveness check and reconnects transparently."""
    return create_engine(config.DW_DATABASE_URL, pool_pre_ping=True)

"""
Delete-then-insert per day,
so reruns are safe.
"""
import pandas as pd
from sqlalchemy import text
import config


def _delete_day(dw_engine, table, date_col, day):
    with dw_engine.begin() as conn:
        conn.execute(text(f"DELETE FROM {table} WHERE {date_col} = :day"), {"day": day})


def load_fact_inventory_snapshot(oltp_engine, dw_engine, snapshot_date=None):
    snapshot_date = snapshot_date or config.SNAPSHOT_DATE

    query = """
        SELECT
            drug_id,
            pharmacy_id,
            price,
            quantity
        FROM pharmacy_inventory
    """
    df = pd.read_sql(query, oltp_engine)
    df.insert(0, "date_key", snapshot_date)

    _delete_day(dw_engine, "fact_inventory_snapshot", "date_key", snapshot_date)
    df.to_sql("fact_inventory_snapshot", dw_engine, if_exists="append", index=False)
    return len(df)


def load_fact_page_views(oltp_engine, dw_engine, day=None):
    day = day or config.SNAPSHOT_DATE

    # "Time" still needs quotes -- it's capitalized in your OLTP table.
    # pharmacy_id no longer needs quotes now that the trailing space is fixed.
    query = text("""
        SELECT
            pharmacy_id,
            CAST("Time" AS DATE) AS date_key,
            COUNT(*) AS number_of_views
        FROM pharmacy_view
        WHERE CAST("Time" AS DATE) = :day
        GROUP BY pharmacy_id, CAST("Time" AS DATE)
    """)
    df = pd.read_sql(query, oltp_engine, params={"day": day})

    _delete_day(dw_engine, "fact_page_views", "date_key", day)
    df.to_sql("fact_page_views", dw_engine, if_exists="append", index=False)
    return len(df)


def load_fact_drug_trends(oltp_engine, dw_engine, day=None):
    day = day or config.SNAPSHOT_DATE

    # search_logs.drug_id is already populated by the fuzzy-search model
    # (single match per search per this schema) and city_id maps directly
    # onto dim_location.location_id -- no join needed to get there.
    query = text("""
        SELECT
            drug_id,
            city_id AS location_id,
            CAST(searched_at AS DATE) AS date_key
        FROM search_logs
        WHERE drug_id IS NOT NULL
          AND city_id IS NOT NULL
          AND CAST(searched_at AS DATE) = :day
    """)
    df = pd.read_sql(query, oltp_engine, params={"day": day})

    if df.empty:
        _delete_day(dw_engine, "fact_drug_trends", "date_key", day)
        return 0

    grouped = (
        df.groupby(["drug_id", "location_id", "date_key"])
        .size()
        .reset_index(name="number_of_searches")
    )

    _delete_day(dw_engine, "fact_drug_trends", "date_key", day)
    grouped.to_sql("fact_drug_trends", dw_engine, if_exists="append", index=False)
    return len(grouped)


def load_all_facts(oltp_engine, dw_engine, day=None):
    day = day or config.SNAPSHOT_DATE
    return {
        "fact_inventory_snapshot": load_fact_inventory_snapshot(oltp_engine, dw_engine, day),
        "fact_page_views": load_fact_page_views(oltp_engine, dw_engine, day),
        "fact_drug_trends": load_fact_drug_trends(oltp_engine, dw_engine, day),
    }
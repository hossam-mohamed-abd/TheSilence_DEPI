import pandas as pd
from upsert import upsert_dataframe


def load_dim_drug(oltp_engine, dw_engine):
    query = """
        SELECT
            d.id AS drug_id,
            d.name AS name,
            dc.name AS category,
            d.manufacturer AS manufacturer
        FROM drugs d
        LEFT JOIN drug_categories dc ON dc.id = d.category_id
    """
    df = pd.read_sql(query, oltp_engine)
    return upsert_dataframe(dw_engine, df, "dim_drug", conflict_cols=["drug_id"])


def load_dim_pharmacy(oltp_engine, dw_engine):
    query = """
        SELECT
            p.id AS pharmacy_id,
            p.name AS name,
            p.phone AS phone,
            p.is_active AS is_active,
            g.name AS governorate,
            c.name AS city
        FROM pharmacies p
        LEFT JOIN cities c ON c.id = p.city_id
        LEFT JOIN governorates g ON g.id = c.governorate_id
    """
    df = pd.read_sql(query, oltp_engine)
    return upsert_dataframe(dw_engine, df, "dim_pharmacy", conflict_cols=["pharmacy_id"])


def load_dim_location(oltp_engine, dw_engine):
    
    query = """
        SELECT
            c.id AS location_id,
            c.name AS city,
            g.name AS governorate,
            co.name AS country
        FROM cities c
        LEFT JOIN governorates g ON g.id = c.governorate_id
        LEFT JOIN countries co ON co.id = g.country_id
    """
    df = pd.read_sql(query, oltp_engine)
    return upsert_dataframe(dw_engine, df, "dim_location", conflict_cols=["location_id"])


def load_dim_date(dw_engine, horizon_days=30):
    from datetime import date, timedelta
    today = date.today()
    dates = [today + timedelta(days=i) for i in range(-horizon_days, horizon_days)]
    df = pd.DataFrame({
        "date_key": [d.isoformat() for d in dates],
        "day_name": [d.strftime("%A") for d in dates],
        "day": [d.day for d in dates],
        "week": [d.isocalendar()[1] for d in dates],
        "month": [d.month for d in dates],
        "quarter": [(d.month - 1) // 3 + 1 for d in dates],
        "year": [d.year for d in dates],
        "is_weekend": [d.strftime("%A") in ("Friday", "Saturday") for d in dates],
    })
    return upsert_dataframe(dw_engine, df, "dim_date", conflict_cols=["date_key"])


def load_all_dimensions(oltp_engine, dw_engine):
    results = {
        "dim_date": load_dim_date(dw_engine),
        "dim_drug": load_dim_drug(oltp_engine, dw_engine),
        "dim_pharmacy": load_dim_pharmacy(oltp_engine, dw_engine),
        "dim_location": load_dim_location(oltp_engine, dw_engine),
    }
    return results
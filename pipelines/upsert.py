from sqlalchemy import Table, MetaData
from sqlalchemy.dialects.postgresql import insert as pg_insert


def upsert_dataframe(engine, df, table_name, conflict_cols):
    """
    Returns the number of rows sent (not necessarily the number changed)
    Postgres upserts a row even if all values are identical).
    """
    if df.empty:
        return 0

    metadata = MetaData()
    table = Table(table_name, metadata, autoload_with=engine)

    records = df.to_dict(orient="records")
    stmt = pg_insert(table).values(records)

    update_cols = {
        c.name: stmt.excluded[c.name]
        for c in table.columns
        if c.name not in conflict_cols
    }
    stmt = stmt.on_conflict_do_update(index_elements=conflict_cols, set_=update_cols)

    with engine.begin() as conn:
        conn.execute(stmt)

    return len(records)

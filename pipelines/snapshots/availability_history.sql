-- snapshots/availability_history.sql
-- Tracks availability changes over time per drug per pharmacy
-- Every time a drug's availability changes in core_pharmacy_inventory,
-- the old record is closed and a new one is inserted
-- This feeds the availability_history table in PostgreSQL
-- and supports:
--   FR-9  (suggest alternatives if drug available in < 3 pharmacies)
--   FR-13 (notify pharmacy if frequently searched drug is unavailable)
--   FR-19 (notify patient when previously unavailable drug is back)
--
-- CHANGES FROM PREVIOUS VERSION
--   Ref updated:     core_drug_prices → core_pharmacy_inventory
--   available col:   was a direct boolean column in core_drug_prices;
--                    now derived as (quantity > 0) since pharmacy_inventory
--                    no longer carries an available column
--   Removed:         price — was never consumed by push_to_postgres.py
--                    for this snapshot (confirmed by column filter in push logic)

{% snapshot availability_history %}

    {{
        config(
            target_schema = 'snapshots',
            unique_key    = 'id',
            strategy      = 'check',
            check_cols    = ['available'],
            invalidate_hard_deletes = True
        )
    }}

    SELECT
        id,
        drug_id,
        pharmacy_id,
        (quantity > 0)  AS available,
        last_updated

    FROM {{ ref('core_pharmacy_inventory') }}

{% endsnapshot %}

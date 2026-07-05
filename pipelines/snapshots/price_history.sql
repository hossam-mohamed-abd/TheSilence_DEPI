-- snapshots/price_history.sql
-- Tracks price changes over time per drug per pharmacy
-- Every time a price changes in core_pharmacy_inventory,
-- the old record is closed and a new one is inserted
-- This feeds the price_history table in PostgreSQL
-- and supports FR-12 (notify patients of price changes)
--
-- CHANGES FROM PREVIOUS VERSION
--   Ref updated: core_drug_prices → core_pharmacy_inventory
--   Removed:     available (column no longer exists in source)

{% snapshot price_history %}

    {{
        config(
            target_schema = 'snapshots',
            unique_key    = 'id',
            strategy      = 'check',
            check_cols    = ['price'],
            invalidate_hard_deletes = True
        )
    }}

    SELECT
        id,
        drug_id,
        pharmacy_id,
        price,
        last_updated

    FROM {{ ref('core_pharmacy_inventory') }}

{% endsnapshot %}

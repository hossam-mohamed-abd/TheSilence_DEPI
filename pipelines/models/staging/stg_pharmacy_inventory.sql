-- models/staging/stg_pharmacy_inventory.sql
-- Reads from seeded pharmacy_inventory table (pharmacy inventory)
-- Column names already standardized by column_normalizer.py
--
-- CHANGES FROM PREVIOUS VERSION (stg_drug_prices.sql)
--   File renamed:    stg_drug_prices.sql → stg_pharmacy_inventory.sql
--   Seed ref:        drug_prices         → pharmacy_inventory
--   Removed:         available (boolean normalization block)
--   Added:           quantity      — defaults to 0 if missing or invalid
--                    minimum_stock — defaults to 0 if missing or invalid
--
-- CORRECTION (post-migration audit):
--   Pharmacies upload drug_id directly (per the ERD — pharmacy_inventory
--   has a drug_id column, not a name column). The original version of
--   this file incorrectly carried over the OLD schema's assumption that
--   pharmacies upload drug names requiring downstream resolution via a
--   join in core_pharmacy_inventory.sql. That resolution step has been
--   removed entirely. drug_id now passes straight through this model.
--
-- ASSUMPTION (to be revisited): pharmacies — or whatever system sits
-- between them and our pipeline — resolve drug names to our internal
-- drug_id before the file reaches Supabase Storage. If that assumption
-- turns out to be false in production, this file needs to be revisited
-- along with core_pharmacy_inventory.sql and core_drugs.sql.
--
-- Availability is derived from quantity in downstream models:
--   available = (quantity > 0)

WITH raw AS (
    SELECT * FROM {{ ref('pharmacy_inventory') }}
),

cleaned AS (
    SELECT
        TRY_CAST(pharmacy_id AS INTEGER)        AS pharmacy_id,

        -- Internal drug ID as provided directly by the pharmacy.
        -- Validated against core_drugs in core_pharmacy_inventory —
        -- rows with an unresolvable drug_id are dropped there.
        TRY_CAST(drug_id AS INTEGER)            AS drug_id,

        -- Default price to 0.0 if null or invalid
        COALESCE(
            TRY_CAST(price AS DOUBLE), 0.0
        )                                       AS price,

        -- Default quantity to 0 if null or invalid
        -- A drug with quantity = 0 is considered unavailable
        COALESCE(
            TRY_CAST(quantity AS INTEGER), 0
        )                                       AS quantity,

        -- Default minimum_stock to 0 if null or invalid
        COALESCE(
            TRY_CAST(minimum_stock AS INTEGER), 0
        )                                       AS minimum_stock,

        -- Use current timestamp if last_updated is missing
        COALESCE(
            TRY_CAST(last_updated AS TIMESTAMP),
            CURRENT_TIMESTAMP
        )                                       AS last_updated

    FROM raw

    WHERE pharmacy_id IS NOT NULL
        AND drug_id IS NOT NULL
),

-- Keep most recent record per pharmacy/drug pair
deduplicated AS (
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY pharmacy_id, drug_id
            ORDER BY last_updated DESC
        ) AS row_num
    FROM cleaned
)

SELECT
    pharmacy_id,
    drug_id,
    price,
    quantity,
    minimum_stock,
    last_updated
FROM deduplicated
WHERE row_num = 1

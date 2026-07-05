-- models/core/core_pharmacy_inventory.sql
-- Builds the final pharmacy_inventory table
-- Generates id as primary key
-- Validates that drug_id exists in core_drugs before including the row
--
-- CHANGES FROM PREVIOUS VERSION (core_drug_prices.sql)
--   File renamed:     core_drug_prices.sql       → core_pharmacy_inventory.sql
--   Staging ref:      stg_drug_prices            → stg_pharmacy_inventory
--   Removed:          available
--   Added:            quantity, minimum_stock
--
-- CORRECTION (post-migration audit):
--   Pharmacies upload drug_id directly (per the ERD). The original
--   version of this model incorrectly resolved drug_id via a
--   LOWER(TRIM(name)) join against core_drugs — that join has been
--   removed. drug_id now passes straight through from staging.
--
--   The INNER JOIN below still exists, but its purpose has changed:
--   it now VALIDATES that the incoming drug_id exists in core_drugs,
--   rather than resolving an ID from a name. Any inventory row whose
--   drug_id does not exist in core_drugs is silently dropped — this
--   was a deliberate decision (confirmed during migration), matching
--   the same pattern already used in core_drug_alternatives.sql for
--   invalid FK pairs. Unlike the old core_drugs.sql, there is no
--   "auto-add unknown drug" fallback here, since there is no drug name
--   to catalogue a new drug from — only a bare ID with no context.
--
-- ASSUMPTION (to be revisited): this assumes pharmacies — or whatever
-- system sits between them and our pipeline — resolve drug names to
-- our internal drug_id before the file reaches Supabase Storage.

WITH staged AS (
    SELECT * FROM {{ ref('stg_pharmacy_inventory') }}
),

-- Validate that drug_id exists in core_drugs before including the row.
-- Rows with an unresolvable drug_id are dropped (not auto-added).
validated AS (
    SELECT
        dp.pharmacy_id,
        dp.drug_id,
        dp.quantity,
        dp.minimum_stock,
        dp.price,
        dp.last_updated

    FROM staged dp

    INNER JOIN {{ ref('core_drugs') }} d
        ON dp.drug_id = d.id
)

SELECT
    ROW_NUMBER() OVER (
        ORDER BY pharmacy_id, drug_id
    )               AS id,
    pharmacy_id,
    drug_id,
    quantity,
    minimum_stock,
    price,
    last_updated

FROM validated

-- models/staging/stg_drugs.sql
-- Reads from seeded drugs table
-- Column names already standardized by column_normalizer.py
-- IMPORTANT: id is trusted from CSV — NOT generated here
--            because drug_alternatives.csv references these exact IDs
--
-- CHANGES FROM PREVIOUS VERSION
--   PK column renamed:    drug_id          → id
--   Column renamed:       active_ingredient → active_substance
--   Added (all nullable): dosage_form, strength, manufacturer,
--                         image_url, created_at, updated_at
--   Deduplication ORDER BY updated:  drug_id → id

WITH raw AS (
    SELECT * FROM {{ ref('drugs') }}
),

cleaned AS (
    SELECT
        TRY_CAST(id AS INTEGER)             AS id,
        TRIM(name)                          AS name,
        TRIM(active_substance)              AS active_substance,
        TRY_CAST(category_id AS INTEGER)    AS category_id,
        TRIM(dosage_form)                   AS dosage_form,
        TRIM(strength)                      AS strength,
        TRIM(manufacturer)                  AS manufacturer,
        TRIM(description)                   AS description,
        TRIM(image_url)                     AS image_url,
        TRY_CAST(created_at AS TIMESTAMP)   AS created_at,
        TRY_CAST(updated_at AS TIMESTAMP)   AS updated_at

    FROM raw

    WHERE name IS NOT NULL
        AND TRIM(name) != ''
        AND id IS NOT NULL
)

-- Deduplicate by drug name — keep the record with the lowest id
-- Prevents duplicate name conflicts from causing FK issues downstream
SELECT *
FROM (
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY LOWER(TRIM(name))
            ORDER BY id
        ) AS row_num
    FROM cleaned
)
WHERE row_num = 1

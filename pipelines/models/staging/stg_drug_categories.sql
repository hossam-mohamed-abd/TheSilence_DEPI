-- models/staging/stg_drug_categories.sql
-- Reads from seeded drug_categories table
-- Column names already standardized by column_normalizer.py
-- IMPORTANT: id is trusted from CSV — NOT generated here
--            because drugs.csv references these exact IDs
--
-- CHANGES FROM PREVIOUS VERSION
--   PK column renamed: category_id → id
--   Added: description (text, nullable)
--   Added: created_at  (timestamp, nullable)
--   Deduplication changed from SELECT DISTINCT → ROW_NUMBER()
--     Reason: DISTINCT broke once nullable columns were added —
--     two rows with the same id/name but different description
--     values would no longer collapse to one row.

WITH raw AS (
    SELECT * FROM {{ ref('drug_categories') }}
),

cleaned AS (
    SELECT
        TRY_CAST(id AS INTEGER)             AS id,
        TRIM(name)                          AS name,
        TRIM(description)                   AS description,
        TRY_CAST(created_at AS TIMESTAMP)   AS created_at

    FROM raw

    WHERE name IS NOT NULL
        AND TRIM(name) != ''
        AND id IS NOT NULL
)

-- Deduplicate by id — keep first occurrence
SELECT
    id,
    name,
    description,
    created_at
FROM (
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY id
            ORDER BY name
        ) AS row_num
    FROM cleaned
)
WHERE row_num = 1

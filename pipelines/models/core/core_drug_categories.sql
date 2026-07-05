-- models/core/core_drug_categories.sql
-- Builds the final drug_categories table
-- IMPORTANT: id comes directly from CSV — NOT generated
--            This ensures drugs.csv FK references (category_id) remain valid
--
-- CHANGES FROM PREVIOUS VERSION
--   PK column renamed: category_id → id
--   Added:             description (text, nullable)
--   Added:             created_at  (timestamp, nullable)

WITH staged AS (
    SELECT * FROM {{ ref('stg_drug_categories') }}
)

SELECT
    id,
    name,
    description,
    created_at

FROM staged

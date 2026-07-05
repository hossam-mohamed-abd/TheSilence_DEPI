-- models/core/core_drugs.sql
-- Builds the final drugs table
-- IMPORTANT: id is trusted directly from the drugs.csv seed —
--            drug_alternatives.csv and pharmacy_inventory both
--            reference these exact IDs.
--
-- CHANGES FROM PREVIOUS VERSION
--   PK column renamed:    drug_id          → id
--   Column renamed:       active_ingredient → active_substance
--   Added (all nullable): dosage_form, strength, manufacturer,
--                         image_url, created_at, updated_at
--
-- REMOVED (post-migration audit):
--   The "auto-add unknown drug from pharmacy inventory" branch has
--   been removed entirely. It previously detected drug NAMES present
--   in pharmacy inventory uploads but absent from drugs.csv, and
--   auto-catalogued them with a placeholder description.
--
--   Per the ERD, pharmacy_inventory carries drug_id directly — there
--   is no drug name in pharmacy uploads to detect an unknown drug from.
--   A drug_id that doesn't exist in this table is now treated as a
--   data integrity error and the corresponding inventory row is
--   silently dropped in core_pharmacy_inventory.sql (confirmed
--   decision, not an oversight).
--
--   This model is now a simple pass-through from stg_drugs. drugs.csv
--   (maintained by the data team) is the single source of truth for
--   the drug catalogue.
--
-- ASSUMPTION (to be revisited): pharmacies — or whatever system sits
-- between them and our pipeline — resolve drug names to our internal
-- drug_id before the file reaches Supabase Storage, and any new drug
-- is catalogued in drugs.csv by the data team before or alongside that
-- resolution. If drugs can legitimately reach us with no prior catalogue
-- entry, an auto-add mechanism (keyed differently, e.g. by manufacturer
-- code) would need to be reintroduced.

WITH staged_drugs AS (
    SELECT * FROM {{ ref('stg_drugs') }}
)

SELECT
    id,
    name,
    active_substance,
    category_id,
    dosage_form,
    strength,
    manufacturer,
    description,
    image_url,
    created_at,
    updated_at

FROM staged_drugs

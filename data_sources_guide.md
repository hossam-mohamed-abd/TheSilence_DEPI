# Data Sources & Collection Guide

This document complements `explain_table.md` and explains **where each type of data comes from**, how it is collected, updated, and validated.

---

## 1) Purpose of this guide

The schema document explains the **data structure**, while this guide explains the **real data source strategy** for each table:
- Primary source (official/operational).
- Ingestion method (API / admin portal / ETL / manual input).
- Update frequency.
- Data quality and validation controls.

---

## 2) Data sources by table

## `manufacturers`
**What we store:** manufacturer name, country, official website.

**Recommended data sources:**
1. Regulatory pharmaceutical authority databases (local drug authority, where available).
2. Official manufacturer websites.
3. Internal master data files (if available).

**Collection method:**
- Import manufacturer lists from official sources (CSV/API) through ETL.
- Add new manufacturers through an admin panel with source documentation.

**Update cadence:** Monthly, or when new manufacturers appear.

**Validation:**
- Prevent duplicates by name + country.
- Validate website format (and optional reachability checks).

---

## `categories`
**What we store:** therapeutic/functional categories (e.g., Antibiotic, Analgesic).

**Recommended data sources:**
1. Standard classification systems (ATC or local equivalent).
2. Internal taxonomy agreed by pharmacy/product teams.

**Collection method:**
- Initialize with seed category dictionary.
- Manage additions/merges via approval workflow (pharmacist + data admin).

**Update cadence:** On-demand, with quarterly review.

**Validation:**
- Category names must be unique.
- Description is optional but recommended for analytics.

---

## `drugs`
**What we store:** drug name, strength, dosage form, manufacturer, category, prescription flag.

**Recommended data sources:**
1. Official regulatory drug registry.
2. Commercial/internal standardized drug database.
3. Approved manufacturer product monographs.

**Collection method:**
- Daily/weekly ingestion from official registry.
- Map each drug to `manufacturer_id` and `category_id` using mapping tables.
- Keep external IDs in staging before final merge.

**Update cadence:** Weekly, or immediately after major regulatory updates.

**Validation:**
- Normalize drug names to reduce duplicate variants.
- Enforce required fields (`name`, `strength`, `form`).
- Verify referenced manufacturer/category exists before insert.

---

## `pharmacies`
**What we store:** pharmacy profile, location, and contact details.

**Recommended data sources:**
1. Partner/onboarding systems.
2. Local licensing records.
3. Direct integrations with pharmacy chain systems.

**Collection method:**
- Onboarding form for new pharmacies.
- Bulk import for pharmacy chains (file/API).
- Geocode address into latitude/longitude.

**Update cadence:**
- Profile fields: when changed.
- Location/hours: monthly review.

**Validation:**
- Phone format validation.
- Ensure coordinates are in valid city/country boundaries.
- Duplicate checks using `(name + address + phone)`.

---

## `drug_inventory`
**What we store:** current price and available stock per drug per pharmacy.

**Recommended data sources:**
1. Pharmacy POS/ERP systems (preferred).
2. Manual partner portal updates for smaller pharmacies.
3. Scheduled batch files (CSV/SFTP).

**Collection method:**
- Real-time API updates on sale/supply/price change events.
- Or scheduled sync every 15–60 minutes.
- For manual edits, log actor + timestamp (audit trail).

**Update cadence:** Near real-time.

**Validation:**
- `unit_price >= 0` and `stock_quantity >= 0`.
- Detect unusual price jumps (anomaly alerts).
- Auto-update `last_updated`.

---

## `drug_alternatives`
**What we store:** therapeutic substitute relationships between drugs.

**Recommended data sources:**
1. Trusted drug knowledge base.
2. Internal clinical/pharmacy review committee.

**Collection method:**
- Initial import from trusted knowledge base.
- Human review for sensitive substitutions.
- Store notes in `substitution_note`.

**Update cadence:** Monthly, or when protocols/guidelines change.

**Validation:**
- Block self-references (`drug_id != alternative_drug_id`).
- Prevent duplicate pairs.
- Optionally enforce bidirectional mappings by policy.

---

## `drug_demand_logs`
**What we store:** time-series demand and sales indicators.

**Recommended data sources:**
1. POS sales transactions (units sold).
2. Unfulfilled requests / out-of-stock attempts (units requested).
3. App/web behavioral signals (search, add-to-cart, failed checkout).

**Collection method:**
- Event streaming or daily batch ingestion from transaction systems.
- Derive `season_tag` automatically from date/location.

**Update cadence:** Daily minimum; hourly preferred for live analytics.

**Validation:**
- `units_sold <= units_requested` (except documented edge cases).
- No negative values.
- Normalize timestamps to a standard timezone.

---

## `medical_services`
**What we store:** list of pharmacy-adjacent medical services.

**Recommended data sources:**
1. Internal service catalog.
2. Partner provider service lists.
3. Ministry/health authority service catalogs (if available).

**Collection method:**
- Start with seed services, then manage through operations team.
- New services require clear description + estimated duration.

**Update cadence:** When new services launch.

**Validation:**
- Service name uniqueness.
- `duration_minutes > 0`.

---

## `service_providers`
**What we store:** entities that provide services (pharmacy, clinic, lab, etc.).

**Recommended data sources:**
1. Partner management system.
2. Official licensing records.
3. Contracting team submissions.

**Collection method:**
- Standard onboarding workflow with required documentation.
- Assign stable internal IDs for each provider.

**Update cadence:** As provider attributes change (address/phone/type).

**Validation:**
- Verify legal identity and license status.
- Validate `provider_type` against a controlled vocabulary.

---

## `service_prices`
**What we store:** service price by provider with validity window.

**Recommended data sources:**
1. Official contracts/pricing agreements.
2. API integration from booking/billing systems.
3. Manual entry with supporting documents.

**Collection method:**
- Ingest prices with validity ranges (`effective_from`, `effective_to`).
- On price changes, create a new record instead of overwriting history.

**Update cadence:** On every pricing change.

**Validation:**
- `price >= 0`.
- Prevent overlapping validity windows for same `(service_id, provider_id)`.
- Validate `currency` as ISO-4217.

---

## 3) Data ingestion channels

1. **Direct API integration**
   - Best for near real-time inventory and pricing.
   - Requires API auth, rate limiting, retries, and monitoring.

2. **Batch ETL (CSV/Excel/SFTP)**
   - Best for master/reference data and non-API partners.
   - Requires schema checks before loading.

3. **Admin portal input**
   - Useful for manual corrections and exceptional cases.
   - Must include complete audit logging.

4. **Streaming events**
   - Best for demand/sales event pipelines.
   - Requires a message broker (e.g., Kafka/RabbitMQ).

---

## 4) Data lifecycle

- **Raw/Staging layer:** data is stored as received.
- **Validation layer:** type/range/relationship/duplicate checks.
- **Curated layer:** approved records used in production tables.
- **Analytics layer:** aggregate marts for reporting/forecasting.

---

## 5) Recommended data quality rules

- **Completeness:** no drug record without manufacturer/category linkage.
- **Uniqueness:** no duplicate natural keys for each domain entity.
- **Consistency:** normalize city/currency/provider-type dictionaries.
- **Timeliness:** monitor freshness, especially for `drug_inventory`.
- **Accuracy:** periodic human sampling + source reconciliation.

---

## 6) Governance and access controls

- Role-based access control (Admin, Analyst, Partner).
- Audit log for sensitive changes (price, inventory, substitutions).
- Encrypt sensitive data in transit and at rest.
- Scheduled backup and recovery testing.

---

## 7) Practical rollout plan

1. Start with master data: `manufacturers`, `categories`, `drugs`.
2. Onboard pharmacy network: `pharmacies`.
3. Integrate stock/pricing: `drug_inventory` (API or batch).
4. Activate demand capture: `drug_demand_logs`.
5. Build services/pricing: `medical_services`, `service_providers`, `service_prices`.
6. Launch dashboards, alerts, and forecasting models.

---

## 8) Critical setup notes

- Define a canonical drug identifier strategy early (internal + external IDs).
- Maintain a shared data dictionary for names and allowed values.
- Agree on SLA targets (e.g., inventory refresh every 15 minutes).
- Start with one city/region as MVP, then expand incrementally.

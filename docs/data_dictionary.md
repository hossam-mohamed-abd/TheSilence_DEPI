# Data Dictionary (Initial)

This dictionary defines foundational entities and expected fields.

## `fact_drug_price`

- `price_event_id` (string, PK)
- `drug_id` (string, FK)
- `pharmacy_id` (string, FK)
- `region_id` (string, FK)
- `observed_at` (timestamp)
- `unit_price_egp` (numeric)
- `source_system` (string)

## `fact_availability`

- `availability_event_id` (string, PK)
- `drug_id` (string, FK)
- `pharmacy_id` (string, FK)
- `in_stock` (boolean)
- `stock_quantity` (integer, nullable)
- `observed_at` (timestamp)

## `dim_drug`

- `drug_id` (string, PK)
- `drug_name_ar` (string)
- `drug_name_en` (string)
- `active_ingredient` (string)
- `atc_code` (string, nullable)
- `manufacturer` (string, nullable)

## `dim_service`

- `service_id` (string, PK)
- `service_type` (enum: lab, radiology)
- `service_name` (string)
- `provider_id` (string)
- `base_price_egp` (numeric)

## Governance Notes

- Owners, SLAs, and quality thresholds must be maintained per table.
- Breaking schema changes require version increment and migration notes.

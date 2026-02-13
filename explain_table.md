# Medical & Pharmacy Intelligence System

## 📌 Project Summary
The **Medical & Pharmacy Intelligence System** is designed to organize and analyze healthcare market data in one integrated database model. The goal is to support better decisions for patients, pharmacies, and healthcare operators by focusing on:

- Drug price tracking across multiple pharmacies.
- Availability and stock monitoring by location.
- Seasonal demand insights for medicines.
- Medical service pricing visibility by provider.
- Analytics-ready structure for affordability, accessibility, and demand behavior.

---

## 🗂️ Database Tables (Conceptual Design)

### 1) `manufacturers`
**Concept:** Stores drug manufacturer details used for traceability and reporting.

| Field | Type | Meaning |
|---|---|---|
| `manufacturer_id` | INT (PK) | Unique manufacturer identifier |
| `name` | VARCHAR | Manufacturer name |
| `country` | VARCHAR | Country of origin |
| `website` | VARCHAR | Official website |
| `created_at` | TIMESTAMP | Record creation time |

### 2) `categories`
**Concept:** Classifies drugs into therapeutic groups.

| Field | Type | Meaning |
|---|---|---|
| `category_id` | INT (PK) | Unique category identifier |
| `name` | VARCHAR | Category title |
| `description` | TEXT | Category explanation |

### 3) `drugs`
**Concept:** Main catalog of medicines, linked to manufacturer and category.

| Field | Type | Meaning |
|---|---|---|
| `drug_id` | INT (PK) | Unique drug identifier |
| `name` | VARCHAR | Drug name |
| `strength` | VARCHAR | Dosage strength |
| `form` | VARCHAR | Form (tablet/syrup/injection...) |
| `manufacturer_id` | INT (FK) | Linked manufacturer |
| `category_id` | INT (FK) | Linked category |
| `is_prescription_required` | BOOLEAN | Whether prescription is required |
| `created_at` | TIMESTAMP | Record creation time |

### 4) `pharmacies`
**Concept:** Stores pharmacy profile and location data.

| Field | Type | Meaning |
|---|---|---|
| `pharmacy_id` | INT (PK) | Unique pharmacy identifier |
| `name` | VARCHAR | Pharmacy name |
| `address` | VARCHAR | Street address |
| `city` | VARCHAR | City |
| `latitude` | DECIMAL | Latitude |
| `longitude` | DECIMAL | Longitude |
| `phone` | VARCHAR | Contact number |
| `is_24_hours` | BOOLEAN | 24/7 status |

### 5) `drug_inventory`
**Concept:** Connects drugs and pharmacies with current stock and price.

| Field | Type | Meaning |
|---|---|---|
| `inventory_id` | INT (PK) | Unique inventory row |
| `drug_id` | INT (FK) | Linked drug |
| `pharmacy_id` | INT (FK) | Linked pharmacy |
| `unit_price` | DECIMAL | Current selling price |
| `stock_quantity` | INT | Available quantity |
| `last_updated` | TIMESTAMP | Last update timestamp |

### 6) `drug_alternatives`
**Concept:** Represents substitute relationships between drugs.

| Field | Type | Meaning |
|---|---|---|
| `drug_id` | INT (FK) | Original drug |
| `alternative_drug_id` | INT (FK) | Alternative drug |
| `substitution_note` | VARCHAR | Clinical/pharmacist note |

### 7) `drug_demand_logs`
**Concept:** Time-based demand records for trend and seasonality analysis.

| Field | Type | Meaning |
|---|---|---|
| `demand_log_id` | BIGINT (PK) | Unique demand record |
| `drug_id` | INT (FK) | Requested drug |
| `pharmacy_id` | INT (FK) | Pharmacy where demand occurred |
| `demand_date` | DATE | Demand date |
| `units_requested` | INT | Total requested units |
| `units_sold` | INT | Total sold units |
| `season_tag` | VARCHAR | Optional season label |

### 8) `medical_services`
**Concept:** Catalog of healthcare services that can be priced and compared.

| Field | Type | Meaning |
|---|---|---|
| `service_id` | INT (PK) | Unique service identifier |
| `service_name` | VARCHAR | Service name |
| `description` | TEXT | Service details |
| `duration_minutes` | INT | Average duration |

### 9) `service_providers`
**Concept:** Entities that provide medical services (pharmacy/clinic/lab).

| Field | Type | Meaning |
|---|---|---|
| `provider_id` | INT (PK) | Unique provider identifier |
| `provider_name` | VARCHAR | Provider name |
| `provider_type` | VARCHAR | Provider classification |
| `city` | VARCHAR | City |
| `phone` | VARCHAR | Contact number |

### 10) `service_prices`
**Concept:** Bridge between services and providers with pricing periods.

| Field | Type | Meaning |
|---|---|---|
| `service_price_id` | INT (PK) | Unique pricing record |
| `service_id` | INT (FK) | Linked service |
| `provider_id` | INT (FK) | Linked provider |
| `price` | DECIMAL | Service price |
| `currency` | CHAR(3) | Currency code |
| `effective_from` | DATE | Start date of validity |
| `effective_to` | DATE | End date of validity |

---

## 🔗 Relationships

### One-to-Many
- `manufacturers` → `drugs`
- `categories` → `drugs`
- `drugs` → `drug_inventory`
- `pharmacies` → `drug_inventory`
- `drugs` → `drug_demand_logs`
- `pharmacies` → `drug_demand_logs`
- `medical_services` → `service_prices`
- `service_providers` → `service_prices`

### Many-to-Many
- `drugs` ↔ `pharmacies` through `drug_inventory`
- `drugs` ↔ `drugs` through `drug_alternatives` (self-reference)
- `medical_services` ↔ `service_providers` through `service_prices`

---

## 🛠️ Example Usage (Business Questions)

- Find the **cheapest pharmacy** for a selected drug.
- Find the **nearest pharmacy with available stock**.
- Analyze **seasonal demand patterns** for top-selling medicines.
- Compare **service prices** between different providers and cities.

---

## ERD / Database Overview (Textual)
At a high level:
1. Drug master data is managed through `drugs`, `manufacturers`, and `categories`.
2. Availability and pricing are managed through `drug_inventory` across `pharmacies`.
3. Substitution logic is modeled through `drug_alternatives`.
4. Demand intelligence is recorded in `drug_demand_logs`.
5. Non-drug medical offerings are modeled through `medical_services`, `service_providers`, and `service_prices`.

This design separates **reference data**, **transactional data**, and **analytics data**, making reporting and expansion easier.

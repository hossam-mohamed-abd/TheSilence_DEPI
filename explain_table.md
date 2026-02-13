# Medical & Pharmacy Intelligence System

## 📌 Project Summary
The **Medical & Pharmacy Intelligence System** is a relational database design focused on improving visibility and decision-making across the healthcare retail ecosystem. It supports:

- Tracking medicine pricing across pharmacies.
- Monitoring drug availability and stock levels by location.
- Recording seasonal and temporal demand patterns.
- Managing medical service offerings and prices by provider.
- Enabling analytics for affordability, accessibility, and demand forecasting.

This model helps pharmacies, health platforms, and analysts answer practical questions such as:

- Which pharmacy currently has the lowest price for a given drug?
- Where is a specific drug in stock near a patient?
- Which medicines surge in demand in winter or flu season?
- How do service prices vary by provider and area?

---

## 🗂️ Database Tables

### 1) `manufacturers`
**Description:** Stores pharmaceutical manufacturer information for drug traceability and reporting.

| Field | Type | Meaning |
|---|---|---|
| `manufacturer_id` | `INT` (PK) | Unique identifier for each manufacturer |
| `name` | `VARCHAR(150)` | Manufacturer name |
| `country` | `VARCHAR(100)` | Country of origin |
| `website` | `VARCHAR(255)` | Official website |
| `created_at` | `TIMESTAMP` | Record creation timestamp |

```sql
CREATE TABLE manufacturers (
    manufacturer_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(150) NOT NULL UNIQUE,
    country VARCHAR(100),
    website VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### 2) `categories`
**Description:** Defines therapeutic or functional drug categories (e.g., Antibiotic, Analgesic, Antihistamine).

| Field | Type | Meaning |
|---|---|---|
| `category_id` | `INT` (PK) | Unique category identifier |
| `name` | `VARCHAR(120)` | Category name |
| `description` | `TEXT` | Category explanation |

```sql
CREATE TABLE categories (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(120) NOT NULL UNIQUE,
    description TEXT
);
```

---

### 3) `drugs`
**Description:** Core drug catalog with references to manufacturer and category.

| Field | Type | Meaning |
|---|---|---|
| `drug_id` | `INT` (PK) | Unique drug identifier |
| `name` | `VARCHAR(180)` | Drug commercial/generic name |
| `strength` | `VARCHAR(80)` | Dosage strength (e.g., 500 mg) |
| `form` | `VARCHAR(80)` | Dosage form (tablet, syrup, injection) |
| `manufacturer_id` | `INT` (FK) | References `manufacturers.manufacturer_id` |
| `category_id` | `INT` (FK) | References `categories.category_id` |
| `is_prescription_required` | `BOOLEAN` | Indicates prescription requirement |
| `created_at` | `TIMESTAMP` | Record creation timestamp |

```sql
CREATE TABLE drugs (
    drug_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(180) NOT NULL,
    strength VARCHAR(80),
    form VARCHAR(80),
    manufacturer_id INT NOT NULL,
    category_id INT NOT NULL,
    is_prescription_required BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_drugs_manufacturer
        FOREIGN KEY (manufacturer_id) REFERENCES manufacturers(manufacturer_id),
    CONSTRAINT fk_drugs_category
        FOREIGN KEY (category_id) REFERENCES categories(category_id)
);
```

---

### 4) `pharmacies`
**Description:** Registry of pharmacies and their location/contact details.

| Field | Type | Meaning |
|---|---|---|
| `pharmacy_id` | `INT` (PK) | Unique pharmacy identifier |
| `name` | `VARCHAR(180)` | Pharmacy name |
| `address` | `VARCHAR(255)` | Street address |
| `city` | `VARCHAR(100)` | City |
| `latitude` | `DECIMAL(10,7)` | Latitude for geospatial search |
| `longitude` | `DECIMAL(10,7)` | Longitude for geospatial search |
| `phone` | `VARCHAR(40)` | Contact number |
| `is_24_hours` | `BOOLEAN` | Open 24/7 flag |

```sql
CREATE TABLE pharmacies (
    pharmacy_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(180) NOT NULL,
    address VARCHAR(255),
    city VARCHAR(100),
    latitude DECIMAL(10,7),
    longitude DECIMAL(10,7),
    phone VARCHAR(40),
    is_24_hours BOOLEAN DEFAULT FALSE
);
```

---

### 5) `drug_inventory`
**Description:** Stock and price table linking drugs to pharmacies (current on-hand quantities and price points).

| Field | Type | Meaning |
|---|---|---|
| `inventory_id` | `INT` (PK) | Unique inventory row identifier |
| `drug_id` | `INT` (FK) | References `drugs.drug_id` |
| `pharmacy_id` | `INT` (FK) | References `pharmacies.pharmacy_id` |
| `unit_price` | `DECIMAL(10,2)` | Price per sale unit |
| `stock_quantity` | `INT` | Quantity available |
| `last_updated` | `TIMESTAMP` | Last stock/price update timestamp |

```sql
CREATE TABLE drug_inventory (
    inventory_id INT PRIMARY KEY AUTO_INCREMENT,
    drug_id INT NOT NULL,
    pharmacy_id INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    stock_quantity INT NOT NULL DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT uq_inventory_drug_pharmacy UNIQUE (drug_id, pharmacy_id),
    CONSTRAINT fk_inventory_drug
        FOREIGN KEY (drug_id) REFERENCES drugs(drug_id),
    CONSTRAINT fk_inventory_pharmacy
        FOREIGN KEY (pharmacy_id) REFERENCES pharmacies(pharmacy_id)
);
```

---

### 6) `drug_alternatives`
**Description:** Maps therapeutically equivalent or substitute drugs.

| Field | Type | Meaning |
|---|---|---|
| `drug_id` | `INT` (FK) | Source drug |
| `alternative_drug_id` | `INT` (FK) | Alternative drug |
| `substitution_note` | `VARCHAR(255)` | Optional pharmacist note |

```sql
CREATE TABLE drug_alternatives (
    drug_id INT NOT NULL,
    alternative_drug_id INT NOT NULL,
    substitution_note VARCHAR(255),
    PRIMARY KEY (drug_id, alternative_drug_id),
    CONSTRAINT chk_not_self_alternative CHECK (drug_id <> alternative_drug_id),
    CONSTRAINT fk_alt_drug
        FOREIGN KEY (drug_id) REFERENCES drugs(drug_id),
    CONSTRAINT fk_alt_alternative
        FOREIGN KEY (alternative_drug_id) REFERENCES drugs(drug_id)
);
```

---

### 7) `drug_demand_logs`
**Description:** Time-series demand records used for seasonal analytics and trend forecasting.

| Field | Type | Meaning |
|---|---|---|
| `demand_log_id` | `BIGINT` (PK) | Unique demand event identifier |
| `drug_id` | `INT` (FK) | Drug being requested/sold |
| `pharmacy_id` | `INT` (FK) | Pharmacy where demand occurred |
| `demand_date` | `DATE` | Date of demand |
| `units_requested` | `INT` | Number of units requested |
| `units_sold` | `INT` | Number of units sold |
| `season_tag` | `VARCHAR(20)` | Optional derived season label (Winter, Summer, etc.) |

```sql
CREATE TABLE drug_demand_logs (
    demand_log_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    drug_id INT NOT NULL,
    pharmacy_id INT NOT NULL,
    demand_date DATE NOT NULL,
    units_requested INT NOT NULL,
    units_sold INT NOT NULL,
    season_tag VARCHAR(20),
    CONSTRAINT fk_demand_drug
        FOREIGN KEY (drug_id) REFERENCES drugs(drug_id),
    CONSTRAINT fk_demand_pharmacy
        FOREIGN KEY (pharmacy_id) REFERENCES pharmacies(pharmacy_id)
);
```

---

### 8) `medical_services`
**Description:** Master list of medical and pharmacy-adjacent services (e.g., blood pressure check, vaccination).

| Field | Type | Meaning |
|---|---|---|
| `service_id` | `INT` (PK) | Unique service identifier |
| `service_name` | `VARCHAR(180)` | Service name |
| `description` | `TEXT` | Service description |
| `duration_minutes` | `INT` | Typical service duration |

```sql
CREATE TABLE medical_services (
    service_id INT PRIMARY KEY AUTO_INCREMENT,
    service_name VARCHAR(180) NOT NULL UNIQUE,
    description TEXT,
    duration_minutes INT
);
```

---

### 9) `service_providers`
**Description:** Service-delivery entities such as clinics, pharmacies, and diagnostic centers.

| Field | Type | Meaning |
|---|---|---|
| `provider_id` | `INT` (PK) | Unique provider identifier |
| `provider_name` | `VARCHAR(180)` | Provider name |
| `provider_type` | `VARCHAR(80)` | Type (Pharmacy, Clinic, Lab) |
| `city` | `VARCHAR(100)` | Provider city |
| `phone` | `VARCHAR(40)` | Contact number |

```sql
CREATE TABLE service_providers (
    provider_id INT PRIMARY KEY AUTO_INCREMENT,
    provider_name VARCHAR(180) NOT NULL,
    provider_type VARCHAR(80) NOT NULL,
    city VARCHAR(100),
    phone VARCHAR(40)
);
```

---

### 10) `service_prices`
**Description:** Many-to-many bridge between `medical_services` and `service_providers`, including current price and validity window.

| Field | Type | Meaning |
|---|---|---|
| `service_price_id` | `INT` (PK) | Unique pricing row identifier |
| `service_id` | `INT` (FK) | References `medical_services.service_id` |
| `provider_id` | `INT` (FK) | References `service_providers.provider_id` |
| `price` | `DECIMAL(10,2)` | Offered price |
| `currency` | `CHAR(3)` | ISO currency code |
| `effective_from` | `DATE` | Price validity start |
| `effective_to` | `DATE` | Price validity end (nullable) |

```sql
CREATE TABLE service_prices (
    service_price_id INT PRIMARY KEY AUTO_INCREMENT,
    service_id INT NOT NULL,
    provider_id INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    currency CHAR(3) NOT NULL DEFAULT 'USD',
    effective_from DATE NOT NULL,
    effective_to DATE,
    CONSTRAINT fk_service_prices_service
        FOREIGN KEY (service_id) REFERENCES medical_services(service_id),
    CONSTRAINT fk_service_prices_provider
        FOREIGN KEY (provider_id) REFERENCES service_providers(provider_id),
    CONSTRAINT uq_service_provider_period UNIQUE (service_id, provider_id, effective_from)
);
```

---

## 🔗 Relationships

### One-to-Many
- **manufacturers → drugs**: one manufacturer can produce many drugs.
- **categories → drugs**: one category can classify many drugs.
- **drugs → drug_inventory**: one drug can appear in many pharmacy inventory rows.
- **pharmacies → drug_inventory**: one pharmacy can stock many drugs.
- **drugs → drug_demand_logs**: one drug can have many demand records.
- **pharmacies → drug_demand_logs**: one pharmacy can generate many demand records.
- **medical_services → service_prices**: one service can have multiple provider prices.
- **service_providers → service_prices**: one provider can publish multiple service prices.

### Many-to-Many
- **drugs ↔ pharmacies** via `drug_inventory`.
- **drugs ↔ drugs** via `drug_alternatives` (self-referencing many-to-many).
- **medical_services ↔ service_providers** via `service_prices`.

### Key Foreign Keys
- `drugs.manufacturer_id → manufacturers.manufacturer_id`
- `drugs.category_id → categories.category_id`
- `drug_inventory.drug_id → drugs.drug_id`
- `drug_inventory.pharmacy_id → pharmacies.pharmacy_id`
- `drug_alternatives.drug_id → drugs.drug_id`
- `drug_alternatives.alternative_drug_id → drugs.drug_id`
- `drug_demand_logs.drug_id → drugs.drug_id`
- `drug_demand_logs.pharmacy_id → pharmacies.pharmacy_id`
- `service_prices.service_id → medical_services.service_id`
- `service_prices.provider_id → service_providers.provider_id`

---

## 🛠️ Example Usage

### 1) Find the cheapest current price for a drug
```sql
SELECT d.name AS drug_name,
       p.name AS pharmacy_name,
       di.unit_price
FROM drug_inventory di
JOIN drugs d ON d.drug_id = di.drug_id
JOIN pharmacies p ON p.pharmacy_id = di.pharmacy_id
WHERE d.name = 'Amoxicillin'
  AND di.stock_quantity > 0
ORDER BY di.unit_price ASC
LIMIT 1;
```

### 2) Find nearest pharmacy with stock (distance approximation)
```sql
SELECT p.pharmacy_id,
       p.name,
       p.address,
       di.stock_quantity,
       di.unit_price,
       (
           6371 * ACOS(
               COS(RADIANS(:user_lat)) * COS(RADIANS(p.latitude))
               * COS(RADIANS(p.longitude) - RADIANS(:user_lng))
               + SIN(RADIANS(:user_lat)) * SIN(RADIANS(p.latitude))
           )
       ) AS distance_km
FROM pharmacies p
JOIN drug_inventory di ON di.pharmacy_id = p.pharmacy_id
JOIN drugs d ON d.drug_id = di.drug_id
WHERE d.name = 'Ibuprofen'
  AND di.stock_quantity > 0
ORDER BY distance_km ASC, di.unit_price ASC
LIMIT 5;
```

### 3) Analyze seasonal demand trends
```sql
SELECT d.name AS drug_name,
       COALESCE(ddl.season_tag,
                CASE
                    WHEN MONTH(ddl.demand_date) IN (12, 1, 2) THEN 'Winter'
                    WHEN MONTH(ddl.demand_date) IN (3, 4, 5) THEN 'Spring'
                    WHEN MONTH(ddl.demand_date) IN (6, 7, 8) THEN 'Summer'
                    ELSE 'Autumn'
                END) AS season,
       SUM(ddl.units_requested) AS total_requested,
       SUM(ddl.units_sold) AS total_sold
FROM drug_demand_logs ddl
JOIN drugs d ON d.drug_id = ddl.drug_id
GROUP BY d.name, season
ORDER BY d.name, total_requested DESC;
```

### 4) Compare service prices by city
```sql
SELECT ms.service_name,
       sp.provider_name,
       sp.city,
       spr.price,
       spr.currency
FROM service_prices spr
JOIN medical_services ms ON ms.service_id = spr.service_id
JOIN service_providers sp ON sp.provider_id = spr.provider_id
WHERE ms.service_name = 'Flu Vaccination'
  AND (spr.effective_to IS NULL OR spr.effective_to >= CURRENT_DATE)
ORDER BY sp.city, spr.price;
```

---

## Notes for Implementation
- Add indexes for high-frequency lookups: `(drug_id, pharmacy_id)`, `(demand_date)`, `(city)`.
- Consider partitioning `drug_demand_logs` by month/year for very large datasets.
- Validate all drug substitutions (`drug_alternatives`) through a pharmacist workflow before activation.

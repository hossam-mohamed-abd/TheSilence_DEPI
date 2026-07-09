# Geographic Data Ingestion Module

This folder contains the automated scripts responsible for database seeding and uploading geopolitical and geographic location datasets (Countries, Governorates/Regions, and Cities) for Egypt and Saudi Arabia.

## 📁 Scripts & Responsibilities

### 1. `upload_to_db (Con&Gov).py`
* **Purpose:** Handles the baseline seeding for the higher-level structural lookup tables: `countries` and `governorates`.
* **Execution Flow:** 1. Reads `countries.csv` and inserts data into the database.
  2. Reads `governorates.csv` and maps each governorate/region to its respective `country_id` (Egypt `country_id = 62` | Saudi Arabia `country_id = 189`).
* **Conflict Resolution:** Utilizes `ON CONFLICT (id) DO NOTHING` to prevent duplicate key errors during re-runs.

### 2. `upload_cities (Egypt-Saudi).py`
* **Purpose:** Uploads the comprehensive parsed city datasets collected from web scraping.
* **Execution Flow:**
  1. Loads `Egy-Sau Cities.xlsx` which contains the compiled scraped records.
  2. Dynamically maps the textual Arabic governorate/region names to their auto-incremented database relational IDs using an internal mapping dictionary (`GOV_MAP`).
  3. Validates mapping completeness and warns about any unmapped region rows before performing a batch insert into the `cities` table.

## 🛠️ Tech Stack & Database Strategy
* **Database:** PostgreSQL (Hosted on Neon Tech).
* **Libraries:** `psycopg2` (with `execute_values` for high-performance chunked batch processing) and `pandas`.
* **Safety:** Transactions are explicitly committed (`conn.commit()`) only after a successful batch operation to prevent partial or corrupted uploads.

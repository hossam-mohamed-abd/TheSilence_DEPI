# Pharmacy Data Ingestion & Incremental Loading Module

This module governs the secure insertion and relational linking of pharmacy inventories, master drug catalogs, and drug categories into the live database. It tracks the migration timeline from the core configuration to delta additions.

## ⚙️ Incremental Load Strategy (Delta Process)
To maximize network efficiency and database performance, **we do not truncate or overwrite existing tables**. When onboarding a new data provider, the ingestion scripts compute the structural delta (difference) and append **only the newly discovered records** without touching preexisting warehouse data.

---

## 📁 Scripts & Architectural Phases

### Phase 1: Baseline Ingestion (`upload_to_db_before_Gar.py`)
* **Target:** Initial pipeline population consisting of **Pharmacy 1, Pharmacy 2, and Pharmacy 3**.
* **Database Coverage:** Fully loads the primary master tables: `drug_categories`, `drugs`, `pharmacies`, and links them with their initial cross-reference records inside `pharmacy_inventory`.
* **Method:** Iterates and batch-inserts the initial CSV records using structural conflict bypass protection.

### Phase 2: Delta Onboarding (`upload_gardenia.py`)
* **Target:** Incremental ingestion of **Pharmacy 4 (Gardenia)**.
* **The Logic (Smart Appending):**
  1. **Categories & Master Drugs:** Instead of pushing the full updated dataset, the script reads both the baseline output and the updated output, computes the programmatic difference (`~df_new["id"].isin(df_old["id"])`), and uploads **ONLY** the absolute new rows.
  2. **Inventory Insulation:** Isolates Gardenia’s unique store ID (`pharmacy_id = 4`) and seamlessly appends its stock records into the broader operational `pharmacy_inventory` table without altering the inventory states of the first three pharmacies.

---

## 🛠️ Technical Implementation Notes
* **Bulk Processing:** Employs `psycopg2.extras.execute_values` to reduce network roundtrips and accelerate heavy transaction ingestion (such as multi-row inventory sets).
* **Data Integrity:** Ensures Python `NaN` values are parsed into database-compliant native `NULL` structures via `.where(pd.notnull(df), None)` transformations before loading.

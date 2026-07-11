# Pharmaceutical Data Engineering & Entity Resolution Pipeline (DEPI Data Lake)

An end-to-end, high-performance data engineering pipeline designed to ingest, clean, normalize, and resolve entities across diverse datasets scraped from four major Egyptian pharmacy networks: **Al-Dawaa, Bloom, Chefaa, and Gardenia**. 

The pipeline implements an advanced **Entity Resolution (Record Linkage)** system using token-based fuzzy matching and the Union-Find algorithm to deduplicate products across competing platforms. The final structured, relational data is mapped to a normalized database schema and loaded into a cloud-hosted PostgreSQL database (Neon Tech).

---

## 🏗️ Architecture & Pipeline Workflow

The pipeline operates in 8 logical phases, structured sequentially to ensure data cleanliness, integrity, and relational validity:

```
[S3 Cloud Data Lake] ──(Ingestion)──> [Pharmacy-Specific Cleaning] ──> [Master Dataset Merge]
                                                                                │
[Neon PostgreSQL] <──(DB Loading)── [Feature & Schema Extraction] <── [Entity Resolution (Fuzzy)]
```

### 1. Data Ingestion & Consolidation
- Connects to an S3-compatible object storage server hosted on **Backblaze B2** using `boto3`.
- Dynamically scans and downloads raw partitioned CSV files for each target pharmacy provider.
- Aggregates and merges multi-part files into single unified datasets (`{pharmacy}_ALL.csv`) while clearing memory and managing local storage footprints.

### 2. Pharmacy-Specific Cleaning & Standardization
Addresses unique structural inconsistencies and formatting anomalies for each platform:
- **Chefaa**: Drops structural metadata (`product_id`, `url`, etc.), applies URL decoding, sanitizes Arabic categories to keep terminal child classifications, and sanitizes descriptions by dropping redundant headings and self-referential brand text.
- **Bloom**: Unescapes nested HTML entities, parses pipelines (`|`) to extract the primary display image, and strips standard text segments like instructions or ingredients out of text fields into structured targets.
- **Gardenia & Al-Dawaa**: Extracts inferred brand headers using fallback title tokens when explicit vendor attributes are missing, standardizes pricing structures, and standardizes alphanumeric text elements.

### 3. Master Consolidation & Schema Normalization
- Merges separate pharmacy outputs into a single **Master Clean Dataset** (`master_clean.csv`).
- Enforces an absolute baseline schema layout across all variants, filling structural voids with empty strings and setting standard currency parameters.

### 4. Entity Resolution & Cross-Pharmacy Matching
Because identical products are named differently across pharmacies (e.g., typos, unit placements, casing variations), an automated clustering sequence is run:
- **Search Key Generation**: Strips volumetric packaging metrics (`ml`, `mg`, `capsule`, `tab`), percentage signs, and punctuation symbols. Standardizes frequent keywords (e.g., `facewash` $
ightarrow$ `face wash`, `spf50` $
ightarrow$ `spf 50`).
- **Candidate Pair Blocking**: Filters dataset comparison pairs using a strict price-blocking window ($\pm 5$ EGP) to avoid exhaustive $O(N^2)$ computations.
- **Fuzzy Score Computation**: Computes an aggregate similarity matrix using the `rapidfuzz` library:
  $$	ext{Final Score} = (	ext{Token Set Ratio} 	imes 0.35) + (	ext{Token Sort Ratio} 	imes 0.25) + (	ext{Partial Ratio} 	imes 0.15) + (	ext{WRatio} 	imes 0.25)$$
- **Disjoint-Set Clustering (Union-Find)**: Chains true positive matches (Threshold $\ge 94\%$) into independent `match_group` IDs.
- **Canonical Name Selection**: Assigns a unified product identity to each group using a weighted criteria matrix (Word token count + word prevalence + pharmacy provider priority index: $	ext{Bloom} > 	ext{Chefaa} > 	ext{Gardenia} > 	ext{Al-Dawaa}$).

### 5. Automated Quality Control & Validation
Generates distinct error and tracking evaluation matrices inside a dedicated reports folder (`downloads/master/reports/`):
- `01_same_name_different_price.csv`: Highlights critical variations ($\Delta > 20$ EGP) for identical items.
- `02_large_groups.csv`: Flags anomalous clusters containing 5 or more interconnected records.
- `03_missing_brand.csv` & `04_missing_category.csv`: Catalogs empty schema fields.
- `05_duplicates.csv`: Highlights row duplicates.

### 6. Relational Feature Extraction
- **Category Matrix**: Generates a unified taxonomy index map (`categories.csv`) allocating sequential category IDs.
- **Clinical Attributation**: Applies optimized Regex patterns over raw strings to distill distinct pharmaceutical fields into a normalized product index (`drugs_ready.csv`):
  - **Strength**: Captures dosage weights (`mg`, `gm`, `mcg`, `iu`, `%`).
  - **Dosage Form**: Extracts clinical mediums (`Tablet`, `Capsule`, `Cream`, `Gel`, `Ointment`, `Syrup`, `Suppository`, etc.).
  - **Marketing Cleanup**: Purges transactional and non-clinical keywords (`Pack`, `Offer`, `Free`, `Promo`, `Original`).

### 7. Cloud Relational Database Loading
Establishes connection bindings via `SQLAlchemy` to seed a live production instances layout:
- Populates `drug_categories` with lookup attributes.
- Maps unique item signatures directly to the master `drugs` table.
- Hydrates the `pharmacy_inventory` transaction table, linking live catalog nodes with physical storefronts (`pharmacy_id`), prices, baseline quantities, and active tracking timestamps (`last_updated = NOW()`).

### 8. Staging Clean Storage
Syncs isolated clean analytical domain files (e.g., `hair-care.csv`) back to secondary staging buckets (`DEPI-Staging-CleanData`) for immediate consuming downstream applications.

---

## 🗄️ Relational Database Schema

The pipeline transforms flat unorganized datasets into a highly structured relational database layout:

```
  ┌───────────────────┐               ┌───────────────────┐
  │  DRUG_CATEGORIES  │               │    PHARMACIES     │
  ├───────────────────┤               ├───────────────────┤
  │ PK │ id           │               │ PK │ id           │
  │    │ name         │               │    │ name         │
  │    │ description  │               └──────────┬────────┘
  └─────────┬─────────┘                          │
            │ 1                                  │ 1
            │                                    │
            │ ∞                                  │ ∞
  ┌─────────┴─────────┐               ┌──────────┴────────┐
  │       DRUGS       │               │PHARMACY_INVENTORY │
  ├───────────────────┤               ├───────────────────┤
  │ PK │ id           │ 1           ∞ │ PK,FK1│ pharmacy_id│
  │ FK │ category_id  ├──────────────>│ PK,FK2│ drug_id   │
  │    │ name         │               │       │ quantity  │
  │    │ manufacturer │               │       │ min_stock │
  │    │ description  │               │       │ price     │
  │    │ image_url    │               │       │ last_upd  │
  │    │ strength     │               └───────────────────┘
  │    │ dosage_form  │
  └───────────────────┘
```

---

## 🛠️ Tech Stack & Dependencies

- **Core Engine**: Python 3.10+ (Jupyter/Colab environment compatible)
- **Data Manipulation**: `pandas` (Vectorized text formatting, grouping, mapping, and merging)
- **Entity Resolution**: `rapidfuzz` (Levenshtein-based token-ratio string matching acceleration)
- **Cloud Infrastructure**: `boto3` (Amazon S3 / Backblaze B2 Object API Integration)
- **Database Architecture**: `SQLAlchemy`, `psycopg2-binary` (PostgreSQL Dialect ORM layer driver)

---

## 🚀 Installation & Setup

1. **Clone the repository and navigate to the project directory:**
   ```bash
   git clone <repository-url>
   cd pharmacy-data-pipeline
   ```

2. **Install all required packages:**
   ```bash
   pip install boto3 pandas rapidfuzz sqlalchemy psycopg2-binary
   ```

3. **Configure Environment Variables / Connection Strings:**
   Update the placeholders within the script with your secure credentials:
   - **Backblaze S3 Credentials**: `aws_access_key_id`, `aws_secret_access_key`, `endpoint_url`.
   - **Neon PostgreSQL URI**: Replace `DATABASE_URL` with your valid Neon cloud connection string.

4. **Run the Notebook/Script:**
   Execute the cells sequentially to trigger the ingestion, processing, entity matching, and database upload workflows.

---

## 📊 Pipeline Reports & Output Verification

Upon successful execution, the following metrics and artifacts are provided:
- **Consolidated Outputs**: Unified datasets saved to `downloads/master/`.
- **Validation Audit Traces**: Located in `downloads/master/reports/` for manual domain-expert review.
- **Database Seeding Confirmations**: Real-time console logs showing success rates, row counts inserted, and data verification totals direct from the live instance.

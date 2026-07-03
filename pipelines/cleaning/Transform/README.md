إليك ملف `README.md` بالتفاصيل الكاملة لكل ملف، بيشرح الـ Logic اللي أنت كاتبه وإزاي حولت صيدليات المرحلة الأولى والصيدلية الرابعة الجديدة:

```markdown
# Pharmacy Data Transformation Module

This module handles the ETL (Extract, Transform, Load) pipeline for integrating disparate data from multiple pharmacies into a unified data structure. It represents the evolution of the ingestion layer as the system scaled from three initial pharmacies to incorporating a fourth one.

---

## 📈 Pipeline Evolution & Workflow

### 1. Phase 1: The Initial Core (`transform_frist_three_pharmacies.py`)
This script was built to handle the structural differences between **Pharmacy 1, Pharmacy 2, and Pharmacy 3**. 
* **Data Standardization:** It reads raw data from these three distinct sources, normalizes column naming conventions, cleans up whitespace, and maps inconsistent formats into a single, standardized DataFrame.
* **Deduplication & Validation:** It drops exact duplicate records, validates essential fields (like drug names and prices), and outputs a consolidated baseline dataset ready for the staging database.

### 2. Phase 2: System Scaling (`add_new_pharmacy.py`)
When **Pharmacy 4** was onboarded, its raw dataset came with a completely different schema and distinct data formatting issues that didn't fit the original script's mapping.
* **Isolation of New Logic:** Instead of hardcoding complex conditional blocks into the stable Phase 1 script, this dedicated script was created to isolate the ingestion logic for the 4th pharmacy.
* **Schema Alignment:** It extracts raw columns from the 4th pharmacy, strips out invalid characters or trailing text, remapps its unique fields to match the master system schema, and appends/merges the newly transformed data into the broader pipeline.

---

## 📁 Technical Specifications

### Technologies Used
* **Python 3.x**
* **Pandas:** For schema mapping, vectorized text cleaning, handling missing data, and merging dataframes.
* **NumPy:** For managing structural data cleaning rules and missing values efficiently.

### File Outputs
Both scripts clean their respective inputs and prepare data to be safely written to the staging layer (`staging_storage.md`) before finalizing into the main database.

---

## 💻 Setup & Execution

### 1. Install Dependencies
Make sure you have `pandas` installed in your environment:
```bash
pip install pandas numpy

```

### 2. Run the Pipelines

To process the baseline data from the initial three stores:

```bash
python transform_frist_three_pharmacies.py

```

To process and integrate the fourth incoming pharmacy dataset:

```bash
python add_new_pharmacy.py

```

---

## ⚠️ Pipeline Rules

* **No Raw Data Modification:** Raw source CSV/Excel files from the pharmacies should never be modified manually. All corrections must happen programmatically inside these scripts.
* **Strict Schema Adherence:** Any new columns introduced by upcoming pharmacies must be explicitly handled via mapping dictionaries inside the code to avoid throwing schema mismatch errors at the database layer.

```

```

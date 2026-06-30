# Data Cleaning Module

## Overview

This folder contains all source code responsible for cleaning, validating, and standardizing data before it is loaded into the Staging Layer and Data Warehouse.

The purpose of this module is to transform raw datasets into structured and reliable data that can be safely used by downstream pipelines.

---

# Responsibilities

The cleaning layer is responsible for:

- Removing duplicates
- Handling missing values
- Fixing invalid records
- Standardizing column names
- Normalizing text values
- Converting data types
- Validating data integrity
- Preparing data for transformation and loading

---

# Data Flow

```text
Raw Data
     ↓
Cleaning Module
     ↓
Staging Layer
     ↓
Warehouse
```

---

# Recommended Structure

```text
cleaning/
│
├── drugs/
│   ├── clean_drugs.py
│   ├── normalize_names.py
│   └── validate_drugs.py
│
├── pharmacies/
│   ├── clean_inventory.py
│   └── validate_inventory.py
│
├── prices/
│   └── clean_prices.py
│
└── shared/
    ├── validators.py
    ├── text_normalization.py
    └── remove_duplicates.py
```

---

# What Should Be Stored Here?

✅ Python cleaning scripts

✅ Validation rules

✅ Reusable cleaning utilities

✅ Data normalization functions

✅ Schema validation code

---

# What Should NOT Be Stored Here?

❌ Raw datasets

❌ CSV files

❌ JSON files

❌ Excel files

❌ Processed datasets

❌ Jupyter notebooks

❌ Documentation unrelated to cleaning

---

# Common Cleaning Operations

Examples:

- Remove duplicate drugs.
- Standardize drug names.
- Convert prices to numeric values.
- Remove invalid inventory records.
- Fix inconsistent text formatting.
- Validate required fields.

---

# Technologies

- Python
- Pandas
- NumPy
- PyArrow
- Regular Expressions (Regex)

---

# Output

The output of this module should always be:

- Clean datasets
- Standardized schemas
- Valid records

These outputs are then passed to:

```text
Staging Layer
```

and later:

```text
Data Warehouse
```

---

# Notes

This folder contains source code only.

All datasets must remain inside:

- Raw Data Storage
- Staging Storage
- Data Warehouse

Never store data files inside the cleaning module.

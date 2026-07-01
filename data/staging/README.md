# Data Cleaning Module

## Overview

The Data Cleaning Module is responsible for cleaning, validating, and standardizing raw datasets before they are loaded into the Staging Storage and later into the Data Warehouse.

This module contains **source code only** and does not store any datasets.

---

# Repository Location

All cleaning scripts are stored inside:

https://github.com/hossam-mohamed-abd/TheSilence_DEPI/tree/main/pipelines/cleaning

This folder contains:

- Data cleaning scripts
- Validation scripts
- Data normalization scripts
- Reusable cleaning utilities

This repository should contain code only.

---

# Staging Storage Documentation

After the datasets are cleaned, they should be uploaded to the project's Staging Storage.

The complete guide for connecting to the storage, authentication, uploading files, downloading files, and managing datasets can be found here:

https://github.com/hossam-mohamed-abd/TheSilence_DEPI/blob/main/infrastructure/staging_storage.md

This document is required for all developers working on the cleaning pipelines.

---

# Purpose

This module is responsible for:

- Removing duplicates
- Handling missing values
- Fixing invalid records
- Standardizing column names
- Normalizing text values
- Converting data types
- Validating data integrity
- Preparing datasets for transformation and loading

---

# Data Flow

```text
Raw Data Storage
        ↓
Cleaning Module
        ↓
Staging Storage
        ↓
Transformation
        ↓
Data Warehouse
```

---

# Input

The cleaning scripts read data from:

```text
Raw Data Storage
```

Documentation:

```text
infrastructure/raw_data_storage.md
```

---

# Output

The output of this module is uploaded to:

```text
DEPI-Staging-CleanData
```

Documentation:

```text
infrastructure/staging_storage.md
```

---

# Recommended Structure

```text
cleaning/
│
├── drugs/
│   ├── clean_drugs.py
│   ├── validate_drugs.py
│   └── normalize_drugs.py
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

# Example Workflow

```text
Download Raw Data
        ↓
Read Dataset
        ↓
Clean & Validate
        ↓
Generate Clean Dataset
        ↓
Upload To Staging Storage
```

---

# Example Cleaning Code

```python
import pandas as pd

df = pd.read_csv("inventory.csv")

df = df.drop_duplicates()

df = df.dropna(
    subset=["drug_name"]
)

df["drug_name"] = (
    df["drug_name"]
    .astype(str)
    .str.strip()
    .str.lower()
)

df.to_parquet(
    "clean_inventory.parquet",
    index=False
)
```

---

# Technologies

- Python
- Pandas
- NumPy
- PyArrow
- Regular Expressions (Regex)

---

# Rules

✅ Store source code only.

✅ Store reusable utilities.

✅ One module per dataset.

❌ Do not store CSV files.

❌ Do not store JSON files.

❌ Do not store Parquet files.

❌ Do not store datasets.

❌ Do not store notebooks.

---

# Responsibilities

This module contains:

- Cleaning Scripts
- Validation Scripts
- Standardization Scripts
- Reusable Utilities

This module does NOT contain:

- Raw Data
- Clean Data
- Historical Data
- Storage Files

---

# Notes

Raw datasets remain inside:

```text
Raw Data Storage
```

Clean datasets are stored inside:

```text
DEPI-Staging-CleanData
```

The official guide for interacting with the staging storage can be found here:

https://github.com/hossam-mohamed-abd/TheSilence_DEPI/blob/main/infrastructure/staging_storage.md

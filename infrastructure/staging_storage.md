# Staging Storage (Clean Data Layer)

## Overview

The Staging Storage is an intermediate storage layer used to store cleaned and validated datasets before they are transformed and loaded into the Data Warehouse.

The MediSearch project uses:

- Backblaze B2 Cloud Storage

Bucket Name:

```text
DEPI-Staging-CleanData
```

This storage contains only clean and standardized datasets.

---

# Purpose

The Staging Storage is responsible for storing:

- Cleaned CSV files
- Validated datasets
- Standardized data
- Intermediate transformation outputs
- Datasets ready for loading into the Data Warehouse

---

# Architecture

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

# What Should Be Stored Here?

✅ Clean CSV files

✅ Clean JSON files

✅ Parquet files

✅ Standardized datasets

✅ Validated data

---

# What Should NOT Be Stored Here?

❌ Raw files

❌ Web scraping outputs

❌ Python scripts

❌ Documentation

❌ Source code

❌ Jupyter notebooks

---

# Recommended Structure

```text
DEPI-Staging-CleanData/
│
├── drugs
│
├── pharmacies
│
├── prices
│
├── inventory
│
└── transformed
```

---

# Technologies Used

- Backblaze B2
- Python
- boto3
- Pandas
- PyArrow

---

# Official Documentation

Backblaze:

https://www.backblaze.com/b2/cloud-storage.html

Documentation:

https://www.backblaze.com/docs

S3 API:

https://www.backblaze.com/docs/cloud-storage-s3-compatible-api

boto3:

https://boto3.amazonaws.com/v1/documentation/api/latest/index.html

---

# Installation

```bash
pip install boto3 pandas pyarrow
```

---

# Environment Variables

```env
B2_ENDPOINT=
B2_KEY_ID=
B2_APPLICATION_KEY=
B2_STAGING_BUCKET=DEPI-Staging-CleanData
```

---

# Connect To Storage

```python
import boto3
import os

s3 = boto3.client(
    service_name="s3",
    endpoint_url=os.getenv("B2_ENDPOINT"),
    aws_access_key_id=os.getenv("B2_KEY_ID"),
    aws_secret_access_key=os.getenv("B2_APPLICATION_KEY")
)
```

---

# Upload Clean Dataset

```python
s3.upload_file(
    "clean_drugs.parquet",
    "DEPI-Staging-CleanData",
    "drugs/clean_drugs.parquet"
)
```

---

# Upload Pharmacy Inventory

```python
s3.upload_file(
    "inventory_clean.csv",
    "DEPI-Staging-CleanData",
    "inventory/el_ezaby_inventory.csv"
)
```

---

# List Files

```python
response = s3.list_objects_v2(
    Bucket="DEPI-Staging-CleanData"
)

for obj in response.get("Contents", []):
    print(obj["Key"])
```

---

# Download File

```python
s3.download_file(
    "DEPI-Staging-CleanData",
    "drugs/clean_drugs.parquet",
    "clean_drugs.parquet"
)
```

---

# Download Entire Folder

```python
response = s3.list_objects_v2(
    Bucket="DEPI-Staging-CleanData",
    Prefix="drugs/"
)

for obj in response.get("Contents", []):
    file_name = obj["Key"].split("/")[-1]

    s3.download_file(
        "DEPI-Staging-CleanData",
        obj["Key"],
        file_name
    )
```

---

# Delete File

```python
s3.delete_object(
    Bucket="DEPI-Staging-CleanData",
    Key="drugs/clean_drugs.parquet"
)
```

---

# Example Workflow

```text
Raw Data
     ↓
Cleaning Scripts
     ↓
Staging Storage
     ↓
Transformation
     ↓
Warehouse Loading
```

---

# Difference Between Raw and Staging

| Feature | Raw Storage | Staging Storage |
|----------|-------------|----------------|
| Original Data | ✅ | ❌ |
| Cleaned | ❌ | ✅ |
| Standardized | ❌ | ✅ |
| Ready For Warehouse | ❌ | ✅ |
| Historical Storage | ✅ | ❌ |
| Reprocessing Source | ✅ | ❌ |

---

# Responsibilities

## Raw Storage

Stores original datasets.

## Staging Storage

Stores clean and validated datasets.

## Data Warehouse

Stores analytics-ready data.

---

# Important Notes

- Never overwrite raw data.
- Use Parquet whenever possible.
- Keep only the latest clean datasets.
- Remove temporary files after loading into the warehouse.
- This storage contains data only.

Source code must remain inside:

```text
pipelines/
```

Documentation must remain inside:

```text
docs/
```

---

# Project Usage

This bucket is used by:

- Cleaning Pipelines
- Transformation Pipelines
- Warehouse Loading Pipelines
- Analytics Pipelines

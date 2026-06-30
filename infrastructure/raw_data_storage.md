# Raw Data Storage (Backblaze B2)

## Overview

The Raw Data Storage is the project's central cloud storage for all raw and historical datasets.

It is implemented using:

- Backblaze B2 Cloud Storage
- S3 Compatible API
- Python + boto3

This storage is considered the primary source of truth for raw files before they are processed by the ETL Pipelines.

---

# Purpose

This storage is used for:

- Web Scraping Results
- Historical Datasets
- Pharmacy Exports
- Logs
- AI Training Datasets
- Processed Data Archives

This storage should ONLY contain data files.

---

# Not Allowed

The following files must NOT be uploaded:

❌ Python files

❌ Jupyter notebooks

❌ Documentation

❌ Source code

❌ ZIP files containing code

❌ Temporary files

❌ Images unrelated to datasets

All code must be stored inside the GitHub Repository.

---

# Recommended Structure

```text
DEPI-data-lake/
│
├── raw
│   ├── pharmacies
│   │   ├── el_ezaby
│   │   ├── seif
│   │   └── rushdy

```

---

# Pharmacy Folder Rules

Each pharmacy must have its own folder.

Example:

```text
raw/pharmacies/el_ezaby/
raw/pharmacies/seif/
raw/pharmacies/rushdy/
```

Inside each folder:

```text
inventory.csv
prices.csv
products.json
metadata.json
```

---

# Environment Variables

```env
B2_ENDPOINT="https://s3.us-east-005.backblazeb2.com"
B2_KEY_ID="0057034b0b8248e0000000001"
B2_APPLICATION_KEY="K005DnwCqFlnsv41kJIREOHF4MsEiE8"
B2_BUCKET_NAME=DEPI-data-lake

```

---

# Installation

```bash
pip install boto3 pandas openpyxl pyarrow
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

# Upload File

```python
s3.upload_file(
    "inventory.csv",
    "DEPI-data-lake",
    "raw/pharmacies/el_ezaby/inventory.csv"
)
```

---

# Upload Scraping Result

```python
s3.upload_file(
    "drugs.json",
    "DEPI-data-lake",
    "raw/scraping/drugs.json"
)
```

---

# List Files

```python
response = s3.list_objects_v2(
    Bucket="DEPI-data-lake"
)

for obj in response.get("Contents", []):
    print(obj["Key"])
```

---

# Download File

```python
s3.download_file(
    "DEPI-data-lake",
    "raw/pharmacies/el_ezaby/inventory.csv",
    "inventory.csv"
)
```

---

# Download Entire Pharmacy Folder

```python
response = s3.list_objects_v2(
    Bucket="DEPI-data-lake",
    Prefix="raw/pharmacies/el_ezaby/"
)

for obj in response.get("Contents", []):
    file_name = obj["Key"].split("/")[-1]

    s3.download_file(
        "DEPI-data-lake",
        obj["Key"],
        file_name
    )
```

---

# Read CSV

```python
import pandas as pd

df = pd.read_csv("inventory.csv")
print(df.head())
```

---

# Read Excel

```python
df = pd.read_excel("inventory.xlsx")
print(df.head())
```

---

# Basic Cleaning Example

```python
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
```

---

# Save Clean Data

CSV:

```python
df.to_csv(
    "clean_inventory.csv",
    index=False
)
```

Parquet:

```python
df.to_parquet(
    "clean_inventory.parquet",
    index=False
)
```

---

# Upload Processed File

```python
s3.upload_file(
    "clean_inventory.parquet",
    "DEPI-data-lake",
    "processed/el_ezaby/clean_inventory.parquet"
)
```

---

# Upload Curated File

```python
s3.upload_file(
    "fact_inventory.parquet",
    "DEPI-data-lake",
    "curated/fact_inventory.parquet"
)
```

---

# Archive File

```python
s3.copy_object(
    Bucket="DEPI-data-lake",
    CopySource={
        "Bucket": "DEPI-data-lake",
        "Key": "raw/pharmacies/el_ezaby/inventory.csv"
    },
    Key="archive/el_ezaby/inventory.csv"
)
```

---

# Delete File

```python
s3.delete_object(
    Bucket="DEPI-data-lake",
    Key="raw/pharmacies/el_ezaby/inventory.csv"
)
```

---

# Typical Workflow

```text
Upload Raw File
        ↓
Download Raw File
        ↓
Data Cleaning
        ↓
Validation
        ↓
Transformation
        ↓
Upload To Processed
        ↓
Upload To Curated
        ↓
Archive
```

---

# Best Practices

✅ Use Parquet whenever possible.

✅ Keep raw files unchanged.

✅ Never overwrite raw datasets.

✅ Store code in GitHub only.

✅ Use environment variables.

✅ Keep one folder per pharmacy.

✅ Keep historical files in archive.

---

# Responsibilities

## Raw Storage

Stores:

- Data
- Datasets
- Logs
- Historical Files

## GitHub Repository

Stores:

- Source Code
- Scrapers
- Pipelines
- Documentation
- Notebooks

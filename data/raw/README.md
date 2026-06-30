# Raw Data Storage Documentation

## Overview

The Raw Data Storage layer is responsible for storing all raw, historical, and unprocessed datasets used by the MediSearch platform.

This storage acts as the primary source of truth for data engineering operations and serves as the entry point for analytics, machine learning, and warehouse pipelines.

---

# Technologies Used

## Cloud Storage

### Backblaze B2 Cloud Storage

Official Website:

https://www.backblaze.com/b2/cloud-storage.html

Documentation:

https://www.backblaze.com/docs/cloud-storage

S3 Compatible API:

https://www.backblaze.com/docs/cloud-storage-s3-compatible-api

---

## Python SDK

### boto3

Documentation:

https://boto3.amazonaws.com/v1/documentation/api/latest/index.html

Installation:

```bash
pip install boto3
```

---

# Why We Chose Backblaze B2

- Free storage tier.
- S3 Compatible API.
- Easy Python integration.
- Suitable for large datasets.
- Simple integration with Data Pipelines.
- Supports historical data storage.

---

# Purpose

The Raw Data Storage is used to store:

- Web Scraping Results
- Historical Datasets
- Pharmacy Exports
- Logs
- Raw CSV Files
- Raw JSON Files
- AI Training Datasets
- Processed Archives

---

# Storage Architecture

```text
Data Sources
        ↓
Raw Data Storage
        ↓
ETL Pipelines
        ↓
Data Warehouse
        ↓
Analytics & AI
```

---

# Folder Structure

```text
DEPI-data-lake/
│
├── raw
│   ├── scraping
│   ├── pharmacies
│   ├── datasets
│   └── logs
│
├── processed
│
├── curated
│
└── archive
```

---

# Environment Variables

```env
B2_ENDPOINT=
B2_KEY_ID=
B2_APPLICATION_KEY=
B2_BUCKET_NAME=DEPI-data-lake
```

---

# Connect To Backblaze

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
    "raw/scraping/drugs.json",
    "drugs.json"
)
```

---

# Delete File

```python
s3.delete_object(
    Bucket="DEPI-data-lake",
    Key="raw/scraping/drugs.json"
)
```

---

# Recommended Data Formats

## CSV

Used for:

- Structured tabular data.

---

## JSON

Used for:

- Nested data.
- API responses.
- Web scraping outputs.

---

## Parquet

Used for:

- Large datasets.
- Analytics.
- Warehouse loading.

---

# Best Practices

✅ Keep raw data unchanged.

✅ Store historical files.

✅ Use folder organization.

✅ Use environment variables.

✅ Separate code from data.

❌ Do not store source code.

❌ Do not store notebooks.

❌ Do not store documentation.

---

# Project Resources

## Backblaze B2

https://www.backblaze.com/b2/cloud-storage.html

## Backblaze Documentation

https://www.backblaze.com/docs/cloud-storage

## boto3 Documentation

https://boto3.amazonaws.com/v1/documentation/api/latest/index.html

## Python

https://www.python.org/

## Pandas

https://pandas.pydata.org/docs/

## Apache Parquet

https://parquet.apache.org/

# Infrastructure Documentation

## Overview

This directory contains all infrastructure documentation used by the MediSearch project.

The purpose of this folder is to centralize all configuration guides, storage documentation, and external services integration in one place.

These documents are intended for:

- Backend Developers
- Data Engineers
- DevOps Engineers
- New Team Members

---

# Folder Structure

```text
infrastructure/
│
├── DatabaseConfigurationGuide_Neon_MainDatabase.md
├── PharmacyIngestionStorage.md
├── raw_data_storage.md
├── staging_storage.md
└── README.md
```

---

# Documents

## DatabaseConfigurationGuide_Neon_MainDatabase.md

Purpose:

Documentation for the Main Operational Database hosted on Neon PostgreSQL.

Contains:

- Database provider information
- Connection instructions
- Environment variables
- Python and Backend connection examples
- Database credentials configuration
- Usage guidelines

Used By:

- Backend
- Data Pipelines
- Warehouse Loading Processes

---

## PharmacyIngestionStorage.md

Purpose:

Documentation for the Pharmacy Landing Zone storage.

Contains:

- Temporary storage architecture
- Upload instructions
- Authentication
- Python integration
- File management

Used By:

- Pharmacy Dashboard
- Ingestion Pipelines

Purpose in Architecture:

```text
Pharmacy
    ↓
Landing Zone
    ↓
Pipeline
```

---

## raw_data_storage.md

Purpose:

Documentation for the Raw Data Lake.

Contains:

- Backblaze B2 configuration
- Authentication
- Upload and download instructions
- Storage structure
- Historical data management
- Python examples

Used By:

- Web Scraping
- Historical Data Storage
- ETL Pipelines
- Analytics
- Machine Learning

Purpose in Architecture:

```text
Data Sources
      ↓
Raw Data Storage
      ↓
ETL Pipelines
```

---

## staging_storage.md

Purpose:

Documentation for the Staging Storage.

Contains:

- Clean data storage configuration
- Authentication
- Upload and download instructions
- Python examples
- Storage organization

Used By:

- Cleaning Pipelines
- Transformation Pipelines
- Warehouse Loading Pipelines

Purpose in Architecture:

```text
Raw Data
      ↓
Cleaning
      ↓
Staging Storage
      ↓
Warehouse
```

---

# High-Level Infrastructure Architecture

```text
Pharmacy Upload
        ↓
Pharmacy Landing Zone
        ↓
Raw Data Storage
        ↓
Cleaning Pipelines
        ↓
Staging Storage
        ↓
Data Warehouse
        ↓
Analytics & AI
```

---

# Responsibilities

This folder contains:

- Infrastructure documentation
- External services configuration
- Storage guides
- Database guides
- Integration instructions

This folder does NOT contain:

- Source code
- Datasets
- Pipelines
- Application logic

---

# Notes

All developers should review the relevant infrastructure document before interacting with:

- Databases
- Cloud Storage
- External Services
- Data Pipelines

The infrastructure documentation acts as the single source of truth for all external resources used by the project.

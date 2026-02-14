# Medical & Pharmacy Intelligence System

A production-focused **Data Engineering platform** for Egypt's healthcare and pharmaceutical ecosystem.

This repository is structured for startup-grade execution by a cross-functional team to ingest, validate, model, and serve insights around:

- Drug price tracking
- Pharmacy availability
- Seasonal demand analysis
- Alternative drugs & active ingredients
- Medical service intelligence (labs, radiology)

---

## 1) Project Overview

The **Medical & Pharmacy Intelligence System** consolidates fragmented medical market data into a governed data platform that powers:

- Operational monitoring (availability and pricing)
- Strategic forecasting (seasonal demand and stock risk)
- Decision-support products (drug alternatives, therapeutic substitutions)
- External/internal consumers (dashboard, APIs, analytics notebooks)

The architecture is designed for iterative growth from MVP to full-scale production with clear boundaries between ingestion, transformation, storage, serving, and governance.

---

## 2) High-Level Architecture (Text Diagram)

```text
                  +---------------------------+
                  |     External Sources      |
                  |---------------------------|
                  | Pharmacy feeds/APIs       |
                  | Supplier lists/prices     |
                  | Public healthcare portals |
                  | Lab & radiology catalogs  |
                  +-------------+-------------+
                                |
                                v
+-------------------------+   Orchestration   +-------------------------+
|  Ingestion Layer        |<----------------->|  Pipeline Scheduler     |
|  (batch/stream/connect) |    (Airflow)      |  retries/lineage/SLAs   |
+------------+------------+                   +------------+------------+
             |                                              |
             v                                              v
+-------------------------+                   +-------------------------+
| Data Lake (Bronze)      |                   | Data Quality &          |
| raw immutable landing   |                   | Validation Checks       |
+------------+------------+                   +------------+------------+
             |                                              |
             v                                              v
+-------------------------+                   +-------------------------+
| Data Lake (Silver/Gold) |------------------>| Warehouse (Dim/Fact)    |
| cleaned/enriched/curated|                   | BI-ready marts          |
+------------+------------+                   +------------+------------+
             |                                              |
     +-------+----------------+                     +-------+-------------+
     |                        |                     |                     |
     v                        v                     v                     v
+------------+         +-------------+      +---------------+    +---------------+
| Analytics  |         | API Layer   |      | Dashboard BI  |    | Data Science  |
| notebooks  |         | FastAPI     |      | app/reporting |    | experimentation|
+------------+         +-------------+      +---------------+    +---------------+
```

---

## 3) Tech Stack (Recommended Baseline)

- **Language**: Python 3.11+
- **Ingestion**: Python connectors, requests/httpx, optional Kafka for events
- **Orchestration**: Apache Airflow
- **Transformation**: SQL + dbt (or SQLMesh), pandas/Polars for targeted jobs
- **Storage**:
  - Data Lake: object/file storage (Bronze/Silver/Gold)
  - Warehouse: PostgreSQL/BigQuery/Snowflake (environment dependent)
- **API**: FastAPI
- **Dashboard**: Streamlit/React + BI embedding (as needed)
- **Infra**: Docker, Terraform
- **CI/CD**: GitHub Actions
- **Quality**: pytest, Great Expectations (optional), schema contracts

---

## 4) Data Sources

Planned source domains:

1. **Pharmacy & Distributor Feeds**
   - Stock availability
   - Retail and wholesale prices
2. **Regulatory/Public Medical Datasets**
   - Drug registrations, active ingredients, approved alternatives
3. **Demand Signals**
   - Historical transactions, seasonal disease indicators, geographic patterns
4. **Medical Service Catalogs**
   - Labs and radiology services, service pricing and location metadata

> Every source should have an owner, ingestion SLA, schema contract, and quality checks documented in `docs/data_dictionary.md`.

---

## 5) Local Development Setup

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Make (optional but recommended)

### Quick Start

```bash
# 1) Clone repository
git clone <repo-url>
cd TheSilence_DEPI

# 2) Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate

# 3) Install dependencies (when requirements are added)
pip install -r requirements.txt

# 4) Configure environment
cp .env.example .env

# 5) Run tests
pytest -q

# 6) Run API (example)
uvicorn api.app.main:app --reload --port 8000

# 7) Run dashboard (example)
streamlit run dashboard/app/main.py
```

---

## 6) Repository Structure

```text
.
├── api/                    # Service layer exposing curated data products
├── dashboard/              # User-facing analytics and monitoring interfaces
├── data/
│   ├── raw/                # Immutable source-aligned extracts
│   ├── external/           # Third-party reference files
│   ├── processed/          # Transitional processed datasets
│   ├── lake/
│   │   ├── bronze/         # Raw standardized landing
│   │   ├── silver/         # Cleaned and conformed data
│   │   └── gold/           # Curated business-ready datasets
│   └── warehouse/          # Exported/load-ready warehouse artifacts
├── docs/                   # Architecture, dictionary, pipeline, deployment docs
├── infra/                  # Docker, Terraform, orchestration configs
├── notebooks/              # Analysis and experimentation notebooks
├── scripts/                # Operational scripts (bootstrap, migrations, helpers)
├── src/
│   ├── ingestion/          # Source connectors and raw loaders
│   ├── pipelines/          # End-to-end orchestration logic
│   ├── transformations/    # Cleansing/business transformation logic
│   ├── storage/            # Warehouse/lake IO abstractions
│   ├── analytics/          # Feature engineering and metric generation
│   ├── utils/              # Shared helper functions
│   └── config/             # Environment/config schema management
├── tests/
│   ├── unit/               # Fast isolated tests
│   ├── integration/        # Pipeline and interface tests
│   └── data_quality/       # Data validation tests and constraints
├── .github/
│   ├── workflows/          # CI/CD workflows
│   ├── pull_request_template.md
│   └── issue_template.md
├── CONTRIBUTING.md
├── GIT_WORKFLOW.md
├── PROJECT_ROADMAP.md
└── README.md
```

---

## 7) Team Operating Model (4 Roles)

- **Data Engineer**
  - Owns ingestion, orchestration, storage modeling, observability
- **Data Analyst**
  - Owns BI metrics, dashboard requirements, validation of business logic
- **Backend Engineer**
  - Owns API contracts, auth, service reliability, integrations
- **Frontend Developer**
  - Owns dashboard UX, interactions, visualization delivery

Shared standards: CI gating, code review, schema versioning, and documented ownership for every pipeline.

---

## 8) Future Roadmap

See [PROJECT_ROADMAP.md](PROJECT_ROADMAP.md) for phased delivery from ingestion MVP to production deployment.

---

## 9) Documentation Index

- [Architecture](docs/architecture.md)
- [Data Dictionary](docs/data_dictionary.md)
- [Pipeline Design](docs/pipeline_design.md)
- [Deployment Guide](docs/deployment_guide.md)
- [Git Workflow](GIT_WORKFLOW.md)
- [Contributing](CONTRIBUTING.md)

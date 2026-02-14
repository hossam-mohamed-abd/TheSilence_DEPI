# Project Roadmap - Medical & Pharmacy Intelligence System

## Phase 1: Data Ingestion

**Objective:** Build reliable source connectors and ingest pipelines.

- Define source inventory and ownership (pharmacies, suppliers, public datasets)
- Implement ingestion adapters in `src/ingestion/`
- Land immutable raw data in `data/raw` and lake bronze
- Add ingestion metadata logging (run time, source latency, record counts)
- Introduce first Airflow DAGs and retry policies

**Exit Criteria**

- All critical sources ingested daily
- Source schema snapshots versioned
- Basic ingestion alerting enabled

---

## Phase 2: Cleaning & Transformation

**Objective:** Standardize and validate ingested data.

- Build cleansing pipelines for nulls, duplicates, outliers
- Normalize key entities (drug name, active ingredient, region, pharmacy ID)
- Implement silver-layer conformance models
- Add data quality rules (freshness, completeness, uniqueness)
- Track bad records and quarantine strategy

**Exit Criteria**

- >95% records pass quality checks on critical tables
- Standardized schemas available for downstream teams

---

## Phase 3: Warehouse Modeling

**Objective:** Deliver analytics-ready dimensional models.

- Design star schema (facts: price, availability, demand; dimensions: drug, location, time)
- Build gold-layer curated marts
- Implement SCD strategy for dimensions where needed
- Define metric layer conventions and naming standards
- Optimize partitioning/indexing strategy

**Exit Criteria**

- Core marts published and query SLAs defined
- Historical trend queries perform within target thresholds

---

## Phase 4: Analytics

**Objective:** Enable business intelligence and predictive insights.

- Create KPI definitions (price volatility, stockout risk, demand index)
- Build analyst-ready semantic outputs
- Create notebooks for cohort/seasonality analysis
- Validate metrics with domain stakeholders

**Exit Criteria**

- Approved KPI catalog and reproducible analytics assets
- Weekly insights reporting workflow operational

---

## Phase 5: Dashboard

**Objective:** Deliver productized insights for end users.

- Build dashboard with role-based views (operations, strategy)
- Add geographic and time-series visualization
- Surface alternative-drug recommendations
- Implement user feedback instrumentation

**Exit Criteria**

- Dashboard available to pilot users
- KPI latency and update cadence meet business expectations

---

## Phase 6: Production Deployment

**Objective:** Harden platform for scale and reliability.

- Infrastructure as code with Terraform modules
- CI/CD with automated testing and deploy gates
- Observability stack: logs, metrics, pipeline alerts
- Backups, disaster recovery, and data retention policies
- Security baselines (secrets management, RBAC, auditability)

**Exit Criteria**

- Production environment approved
- SLO/SLA baselines defined and monitored
- On-call runbook and incident process documented

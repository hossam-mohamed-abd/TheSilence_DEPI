# Pipeline Design

## Pipeline Pattern

Each domain pipeline follows:

1. `extract_*` - Source pull and raw persistence
2. `validate_raw_*` - Contract and freshness checks
3. `transform_silver_*` - Standardization and cleansing
4. `transform_gold_*` - KPI-ready curation
5. `load_warehouse_*` - Warehouse loading and indexing
6. `publish_*` - API/dashboard refresh triggers

## Orchestration Conventions

- Schedule: source-dependent (hourly/daily)
- Idempotency: required for all load tasks
- Retries: exponential backoff
- Failure policy: fail fast on contract violations; quarantine bad records

## Data Quality Gates

- Mandatory checks: schema, null thresholds, uniqueness, freshness
- Optional checks: distribution drift, anomaly bounds
- Quality reports stored per run for auditability

## Observability

- Metrics: rows in/out, error rate, latency
- Logging: structured logs with pipeline run IDs
- Alerting: stale data, failed DAG, high invalid record ratio

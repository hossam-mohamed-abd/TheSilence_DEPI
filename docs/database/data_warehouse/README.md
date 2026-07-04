# MediSearch Data Warehouse Documentation

## Purpose

The MediSearch data warehouse is the OLAP data store for analytics, historical reporting, KPI tracking, business intelligence, and AI feature preparation. It is implemented using Neon PostgreSQL as a separate database from the main operational OLTP database.

The warehouse organizes operational and external data into analytical structures such as dimension tables, fact tables, historical snapshots, aggregated metrics, and KPI summaries.

## Contents

| File | Description |
| --- | --- |
| `star_schema.mmd` | Professional star schema diagram with conformed dimensions and analytical fact tables. |
| `fact_dimension_relationships.mmd` | Relationship diagram connecting dimensions, facts, analytics outputs, KPIs, and AI features. |
| `warehouse_flow.mmd` | Data processing flow from raw storage through cleaning, staging, transformation, warehouse, and analytics. |
| `README.md` | This guide for understanding the warehouse documentation. |

## Diagrams

### `star_schema.mmd`

Shows the analytical model with central fact tables and surrounding dimensions. It documents the intended BI-ready structure for search analytics, inventory snapshots, user engagement, drug availability, and daily KPI summaries.

### `fact_dimension_relationships.mmd`

Explains how dimensions provide business context to fact tables and how those facts feed analytics use cases, KPIs, and AI feature inputs.

### `warehouse_flow.mmd`

Illustrates the warehouse processing lifecycle from raw storage to cleaned data, staging models, transformations, warehouse tables, and analytics outputs.

## How to Read the Documentation

1. Start with `warehouse_flow.mmd` to understand the data pipeline stages.
2. Review `star_schema.mmd` to understand the dimensional model.
3. Review `fact_dimension_relationships.mmd` to connect the dimensional model to analytics, KPIs, and AI use cases.
4. Treat all diagrams as architecture documentation. They are Mermaid diagrams only and are not SQL scripts or generated ERD images.

## Related Documents

- `../README.md` — parent database documentation index.
- `../main_database/README.md` — operational database documentation.
- `../shared/README.md` — shared lifecycle documentation.
- `../../data_engineering/warehouse/README.md` — warehouse engineering context.
- `../../architecture/warehouse/README.md` — warehouse architecture context.

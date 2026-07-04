# MediSearch Database Documentation

## Purpose

This directory contains enterprise architecture documentation for the two separate MediSearch database platforms:

1. **Main Operational Database (OLTP)** — a Neon PostgreSQL database that supports the live web application.
2. **Data Warehouse (OLAP)** — a Neon PostgreSQL analytics database that stores curated, historical, aggregated, and AI-ready data.

The documentation is designed for database architects, backend engineers, data engineers, analytics engineers, technical reviewers, and graduation project evaluators.

## Contents

| Area | Description |
| --- | --- |
| `main_database/` | Operational database documentation for users, pharmacies, drugs, inventory, favorites, notifications, and search logs. |
| `data_warehouse/` | Analytical warehouse documentation for fact tables, dimensions, KPIs, BI, and AI feature support. |
| `shared/` | Cross-database lifecycle documentation that explains how data moves from sources to analytics and AI. |

## Diagrams

| Diagram | Location | Purpose |
| --- | --- | --- |
| Main database overview | `main_database/database_overview.mmd` | Shows how users, the Angular frontend, backend services, and the OLTP database interact. |
| Main schema relationships | `main_database/schema_relationships.mmd` | Shows the major operational entities and their relationships using Mermaid ER syntax. |
| Warehouse star schema | `data_warehouse/star_schema.mmd` | Shows fact tables, dimension tables, and analytical relationships. |
| Fact and dimension relationships | `data_warehouse/fact_dimension_relationships.mmd` | Connects facts and dimensions to analytics outputs and KPIs. |
| Warehouse flow | `data_warehouse/warehouse_flow.mmd` | Shows the OLAP pipeline from raw storage to analytics. |
| Shared data lifecycle | `shared/data_lifecycle.mmd` | Shows the complete data lifecycle from external sources through AI outputs. |

## How to Read the Documentation

1. Start with `main_database/database_overview.mmd` to understand the operational database role in the web application.
2. Review `main_database/schema_relationships.mmd` to understand the core OLTP entities and relationships.
3. Move to `data_warehouse/warehouse_flow.mmd` to understand how analytics-ready data is prepared.
4. Review `data_warehouse/star_schema.mmd` and `data_warehouse/fact_dimension_relationships.mmd` to understand analytical modeling, facts, dimensions, KPIs, and BI usage.
5. Finish with `shared/data_lifecycle.mmd` to understand the complete end-to-end data journey.

## Related Documents

- `../data_engineering/` — pipeline, cleaning, ETL, analytics, and warehouse documentation.
- `../architecture/warehouse/` — warehouse architecture context.
- `../diagrams/database/` — additional database diagram references.
- `../deployment/DatabaseConfigurationGuide.md` — database configuration and deployment guidance.

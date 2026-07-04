# MediSearch Shared Database Documentation

## Purpose

This directory contains documentation that applies across both MediSearch databases: the main operational OLTP database and the analytical OLAP data warehouse. It focuses on the complete data lifecycle rather than a single physical database.

## Contents

| File | Description |
| --- | --- |
| `data_lifecycle.mmd` | End-to-end lifecycle diagram from external sources through raw data, cleaning, staging, warehouse, analytics, and AI. |
| `README.md` | This guide for understanding shared database documentation. |

## Diagrams

### `data_lifecycle.mmd`

Shows the complete MediSearch data lifecycle. It begins with external sources and operational feeds, moves through raw storage, cleaning, staging, and the warehouse, then supports analytics and AI capabilities.

## How to Read the Documentation

1. Use this section after reviewing the operational and warehouse-specific documentation.
2. Read `data_lifecycle.mmd` to understand how data progresses across systems and why each processing stage exists.
3. Interpret the diagram as a conceptual lifecycle model for documentation and architecture review, not as an executable pipeline or SQL implementation.

## Related Documents

- `../README.md` — parent database documentation index.
- `../main_database/README.md` — main operational database documentation.
- `../data_warehouse/README.md` — data warehouse documentation.
- `../../data_engineering/README.md` — broader data engineering documentation.

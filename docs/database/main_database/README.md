# MediSearch Main Operational Database Documentation

## Purpose

The main operational database is the OLTP data store for the MediSearch web application. It is implemented using Neon PostgreSQL and supports real-time application operations such as user management, pharmacy management, drug search, inventory lookup, favorites, notifications, and search logging.

This database is optimized for transactional consistency, application reliability, and direct backend service access.

## Contents

| File | Description |
| --- | --- |
| `database_overview.mmd` | High-level application-to-database architecture diagram. |
| `schema_relationships.mmd` | Mermaid ER diagram for the major operational entities. |
| `README.md` | This guide for understanding the main database documentation. |

## Diagrams

### `database_overview.mmd`

Shows the operational path from MediSearch users to the Angular frontend, backend API services, and the main Neon PostgreSQL database. It also summarizes the operational domains stored in the database, including users, pharmacies, drugs, inventory, favorites, notifications, and search logs.

### `schema_relationships.mmd`

Uses Mermaid ER diagram syntax to document how the major OLTP entities relate to each other. The diagram highlights relationships such as users saving favorite drugs, pharmacies maintaining inventory, drugs belonging to categories, and search logs capturing user search behavior.

## How to Read the Documentation

1. Read `database_overview.mmd` first to understand where the database sits in the web application architecture.
2. Read `schema_relationships.mmd` next to understand the entity model and relationship cardinalities.
3. Use the entity names as logical documentation concepts rather than generated SQL definitions. These diagrams do not create database objects and are not SQL migration scripts.

## Related Documents

- `../README.md` — parent database documentation index.
- `../data_warehouse/README.md` — analytical data warehouse documentation.
- `../shared/README.md` — shared lifecycle documentation.
- `../../deployment/DatabaseConfigurationGuide.md` — deployment and configuration context.

# Database Reference

## Overview

MediSearch uses PostgreSQL for the operational application database and documents warehouse structures for analytics. The backend accesses PostgreSQL through Prisma Client.

## Purpose

This reference summarizes the implemented database domains, relationships, and operational considerations for developers and data engineers.

## Contents

- Operational database domains
- Key relationships
- Application tables
- Analytics tables
- Data integrity notes
- Related documents

## Operational Database Domains

| Domain | Tables |
| --- | --- |
| Identity | `users`, `pharmacy_staff` |
| Geography | `countries`, `governorates`, `cities` |
| Medicine catalog | `drug_categories`, `drugs`, `drug_tags`, `drug_alternatives` |
| Pharmacy operations | `pharmacies`, `pharmacy_inventory`, `pharmacy_ratings` |
| User engagement | `favorites`, `notifications`, `search_logs` |
| Monitoring and analytics | `alerts`, `availability_history`, `price_history`, `drug_analytics` |

## Key Relationships

- Countries contain governorates; governorates contain cities.
- Cities are referenced by users, pharmacies, and search logs.
- Drug categories classify drugs.
- Pharmacy inventory joins pharmacies to drugs and stores quantity, minimum stock, price, and last update.
- Users can favorite drugs and review pharmacies.
- Notifications belong to users.
- Alerts can reference drugs and pharmacies.
- Price and availability history support trend analysis.

## Application Tables

### Users and Authentication

`users` stores identity, contact details, password hashes, role, city, active status, profile image, verification status, and login timestamps.

### Medicine Catalog

`drugs` stores medicine name, active substance, dosage form, strength, manufacturer, description, image, timestamps, and category reference.

### Pharmacy Inventory

`pharmacy_inventory` is the core availability table. It enforces a unique pharmacy/drug pair and stores quantity, minimum stock, price, and last updated timestamp.

### Favorites and Notifications

`favorites` enforces one favorite per user/drug pair. `notifications` stores user-specific messages and read state.

## Analytics Tables

- `price_history` records historical prices by drug and pharmacy.
- `availability_history` records availability checks by drug and pharmacy.
- `drug_analytics` stores calculated price and availability summaries.
- `search_logs` supports demand and search behavior analysis.

## Data Integrity Notes

- Use foreign keys to preserve relationship integrity.
- Preserve unique constraints on favorites, inventory, alternatives, and pharmacy ratings.
- Validate imported ETL rows before insertion to avoid orphaned IDs.
- Use indexes on frequent search and join fields such as drug name, active substance, category, inventory drug/pharmacy IDs, and search text.

## Related Documents

- [Main Database README](main_database/README.md)
- [Warehouse README](warehouse/README.md)
- [Data Warehouse README](data_warehouse/README.md)
- [Data Lifecycle](../data_engineering/PIPELINES_AND_DATA_LIFECYCLE.md)

## Notes

The Prisma schema is the application-facing source of truth for backend model names and relationships. Database diagrams in this folder are generated references and should not be edited unless diagram regeneration is explicitly requested.

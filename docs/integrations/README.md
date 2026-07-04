# Integration Documentation

## Overview

MediSearch integrates browser clients, backend APIs, PostgreSQL databases, scraping sources, ETL scripts, and deployment services into a single medicine search and pharmacy intelligence platform.

## Purpose

This document explains the main integration points, expected contracts, and handoff boundaries between subsystems.

## Contents

- Frontend-to-backend integration
- Backend-to-database integration
- Scraping and ETL integration
- Warehouse integration
- External deployment integration

## Frontend to Backend

The Angular frontend communicates with the Express API using `HttpClient` services in `core/services`.

Key integrations:

- `AuthService` -> `/auth`, `/countries`, `/governorates`, `/cities`
- `CategoryService` -> `/categories/home`
- `MedicineService` -> `/home/medicines/featured`
- `PharmacyService` -> `/home/pharmacies`
- `SearchService` -> `/search`
- `FavoriteService` -> `/favorites`
- `NotificationService` -> `/notifications`
- `StatisticsService` -> `/home/statistics`

Cookie-protected endpoints must be called with credentials enabled.

## Backend to Database

The backend uses Prisma Client with PostgreSQL. Feature repositories query tables for users, drugs, pharmacies, inventory, ratings, favorites, notifications, geography, search logs, analytics, price history, and availability history.

Integration contract:

- Prisma schema is the application database contract.
- Repository methods hide query details from controllers.
- BigInt IDs are serialized before sending JSON responses.
- Database connection strings are supplied through environment variables.

## Scraping and ETL

Scraping scripts collect source data from pharmacy and drug websites. Cleaning and upload scripts normalize geography, pharmacy, drug, and inventory data before inserting into PostgreSQL.

Recommended contract between stages:

1. Raw source output is immutable.
2. Staging output is cleaned and validated.
3. Upload scripts enforce required fields and relationship IDs.
4. Warehouse loads use validated operational data.

## Warehouse Integration

The warehouse supports analytics and reporting. It should be loaded from trusted operational or staging tables, not directly from unvalidated raw scrape outputs.

Typical metrics:

- Medicine availability by pharmacy and location.
- Price ranges and price history.
- Category coverage.
- Search popularity.
- Pharmacy inventory and rating summaries.

## External Deployment Integration

The project references Vercel-style deployment for web assets and backend functions. Production integration requires:

- Correct frontend build output.
- Backend environment variables in deployment settings.
- CORS configured for deployed frontend domains.
- Database provider SSL and connection limits configured.

## Related Documents

- [API Reference](../api/API_REFERENCE.md)
- [Architecture Documentation](../architecture/README.md)
- [Data Engineering Documentation](../data_engineering/README.md)
- [Deployment Guide](../deployment/README.md)

## Notes

When an integration contract changes, update both producer and consumer documentation in the same pull request.

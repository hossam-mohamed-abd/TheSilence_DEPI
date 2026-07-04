# Development Guide

## Overview

MediSearch is organized as an Angular frontend, an Express/TypeScript backend, PostgreSQL database assets, Python scraping and ETL pipelines, and documentation under `docs`.

## Purpose

This guide helps new contributors set up the project, understand the repository layout, run core services, and make changes safely.

## Contents

- Repository layout
- Local setup
- Backend workflow
- Frontend workflow
- Data engineering workflow
- Coding standards
- Contribution checklist

## Repository Layout

| Path | Responsibility |
| --- | --- |
| `web_app/frontend` | Angular application, pages, shared components, services, guards, and models. |
| `web_app/Backend` | Express API, Prisma schema, modules, middleware, repositories, and services. |
| `web_scaping` | Source-specific scraping scripts for pharmacy and drug data. |
| `pipelines` | Cleaning, transformation, and upload scripts. |
| `database` | Database schema references, migrations, and seeds. |
| `infrastructure` | Deployment, storage, and Neon database setup notes. |
| `docs` | Enterprise project documentation. |
| `tests` | Test assets and future automated test suites. |

## Local Setup

1. Install Node.js and npm compatible with the frontend and backend lockfiles.
2. Install Python for scraping and pipeline scripts.
3. Create backend environment variables for `DATABASE_URL`, `JWT_SECRET`, `NODE_ENV`, and `PORT`.
4. Install backend dependencies with `npm install` from `web_app/Backend`.
5. Install frontend dependencies with `npm install` from `web_app/frontend`.
6. Prepare the database and generate the Prisma client.

## Backend Workflow

Run from `web_app/Backend`:

```bash
npm install
npm run build
npm run dev
```

Key implementation conventions:

- `src/app.ts` wires middleware and route modules.
- `src/server.ts` starts the HTTP server.
- Each feature module is organized by route, controller, service, and repository.
- Prisma access is centralized through the Prisma client configuration and repositories.
- Protected routes use `authMiddleware`.

## Frontend Workflow

Run from `web_app/frontend`:

```bash
npm install
npm start
npm run build
npm test
```

Key implementation conventions:

- Routes are declared in `src/app/app.routes.ts`.
- Shared UI lives under `components/shared`.
- Home-page sections live under `components/home/components`.
- API access is isolated in `core/services`.
- TypeScript interfaces live in `core/models`.
- Lightweight client state uses Angular signals and RxJS where appropriate.

## Data Engineering Workflow

- Scrapers collect raw source data.
- Cleaning scripts normalize fields and prepare staging outputs.
- Upload scripts load geography, pharmacy, and medicine data into PostgreSQL.
- Warehouse documentation describes analytical tables and relationships.

## Coding Standards

- Keep frontend services thin and typed.
- Keep backend controllers focused on HTTP concerns.
- Put business logic in services and data access in repositories.
- Validate user input before persistence.
- Do not log passwords, tokens, or database credentials.
- Keep documentation updates in the `docs` directory.

## Contribution Checklist

- [ ] Read related documentation before changing code.
- [ ] Update or add docs for behavior changes.
- [ ] Run affected build and test commands.
- [ ] Confirm no secrets or generated local files are committed.
- [ ] Document known limitations in the relevant README.

## Related Documents

- [Frontend Documentation](../frontend/README.md)
- [Backend Documentation](../backend/README.md)
- [Testing Documentation](../testing/README.md)
- [API Reference](../api/API_REFERENCE.md)

## Notes

This guide documents the current project shape and should be revised whenever folders, frameworks, commands, or development processes change.

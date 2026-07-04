# Configuration Guide

## Overview

MediSearch configuration is split across the Angular frontend, Express backend, Prisma database layer, deployment settings, and Python data pipelines.

## Purpose

This guide explains which configuration values are required, where they are consumed, and how to keep local, staging, and production environments consistent.

## Contents

- Required backend variables
- Frontend environment values
- Database configuration
- Pipeline configuration
- Configuration checklist

## Backend Configuration

The backend is a Node.js/TypeScript Express application. It requires at minimum:

| Variable | Purpose | Example |
| --- | --- | --- |
| `DATABASE_URL` | PostgreSQL connection string consumed by Prisma. | `postgresql://user:password@host/db?sslmode=require` |
| `JWT_SECRET` | Secret used to sign and verify JWT tokens. | Use a long random secret. |
| `NODE_ENV` | Controls production cookie behavior and runtime mode. | `development` or `production` |
| `PORT` | API port when running locally. | `3000` |

## Frontend Configuration

Angular stores environment-specific values in `src/environments`.

| File | Purpose |
| --- | --- |
| `environment.ts` | Local development settings. |
| `environment.prod.ts` | Production API settings. |

The primary value is `apiUrl`, which should point to the backend `/api` base path.

## Database Configuration

The Prisma datasource uses `DATABASE_URL`. Database structure is described by the Prisma schema and supporting database documentation.

Recommended practices:

- Use separate databases for local development, staging, production, and warehouse workloads.
- Use SSL for managed PostgreSQL providers.
- Keep migration and schema documentation aligned.
- Avoid running destructive scripts against production without backup and approval.

## Pipeline Configuration

Python scraping and ETL scripts should use environment variables for database credentials, source URLs, output paths, and upload settings. Raw, staging, and warehouse locations should remain separate.

## Configuration Checklist

- [ ] Backend `.env` exists locally and is not committed.
- [ ] Production secrets are configured in the deployment platform.
- [ ] Frontend `apiUrl` matches the deployed backend URL.
- [ ] CORS allow-list includes only trusted frontend domains.
- [ ] Prisma client is regenerated after schema changes.
- [ ] Pipeline credentials are separate from application credentials.

## Related Documents

- [Deployment Guide](../deployment/README.md)
- [Database Configuration Guide](../deployment/DatabaseConfigurationGuide.md)
- [Backend Documentation](../backend/README.md)
- [Data Engineering Documentation](../data_engineering/README.md)

## Notes

Do not store real production credentials in documentation. Use placeholders and describe required values instead.

# Operations, Monitoring, and Troubleshooting Guide

## Overview

MediSearch operations cover the deployed frontend, backend API, PostgreSQL database, data-import jobs, and documentation artifacts needed to support the system after release.

## Purpose

This guide gives maintainers a practical runbook for monitoring, incident response, backups, common failures, and troubleshooting.

## Contents

- Operational components
- Health checks
- Monitoring recommendations
- Backup and recovery
- Troubleshooting runbook
- FAQ

## Operational Components

| Component | Runtime Concern |
| --- | --- |
| Angular frontend | Availability, correct API URL, browser compatibility, static asset delivery. |
| Express backend | API uptime, CORS, cookies, JWT validation, Prisma connectivity. |
| PostgreSQL main database | Connection limits, data integrity, backups, index health. |
| Data warehouse | Analytical freshness, load success, schema consistency. |
| Scraping and ETL scripts | Source availability, throttling, clean transformation, failed uploads. |

## Health Checks

- API root: `GET /`
- API health: `GET /api/health`
- Frontend: load the home page and confirm categories, featured medicines, pharmacies, and statistics render.
- Database: run a low-cost read query through Prisma or the database provider console.

## Monitoring Recommendations

Track these signals in production:

- API request count, latency, status codes, and error rates.
- Authentication failures and repeated login attempts.
- Database connection usage and slow queries.
- Scraping job duration, source failures, and row counts by stage.
- Warehouse load freshness and validation failures.
- Frontend JavaScript errors and failed API calls.

## Backup and Recovery

- Enable managed PostgreSQL backups.
- Export critical warehouse snapshots before major transformation changes.
- Test restore procedures before production release.
- Keep raw scraped files long enough to rebuild staging and warehouse outputs.
- Record deployment versions, schema versions, and pipeline versions.

## Troubleshooting Runbook

### Frontend cannot call the API

1. Confirm `environment.apiUrl` points to the expected `/api` base URL.
2. Confirm backend CORS allow-list includes the frontend origin.
3. Confirm browser requests include credentials where cookies are required.
4. Check API health endpoint.

### Login succeeds but protected pages fail

1. Check whether the `token` cookie is present.
2. Verify cookie `secure` and `sameSite` settings match local or production mode.
3. Confirm `JWT_SECRET` is the same for signing and verification.
4. Inspect backend `401` responses for missing or invalid token messages.

### Prisma cannot connect

1. Validate `DATABASE_URL` format.
2. Confirm network access to the database provider.
3. Confirm database user permissions.
4. Regenerate Prisma client after schema changes.

### Search or pharmacy inventory appears incomplete

1. Verify operational tables contain current pharmacy inventory rows.
2. Check category and drug relationships.
3. Check ETL load logs and row counts.
4. Confirm query filters such as `available=true` are not hiding rows.

### Scraping jobs fail

1. Check whether the source website changed markup or blocking behavior.
2. Reduce request concurrency and add retries/backoff.
3. Validate raw output before running transformations.
4. Keep failed source examples for parser updates.

## FAQ

### Is MediSearch a medical diagnosis system?

No. It is a medicine/pharmacy discovery, availability, and intelligence platform. Medical content should be treated as informational and reviewed by qualified professionals before clinical use.

### Where should new documentation go?

Use the most specific folder under `docs`. Add a new README only when it improves navigation and does not duplicate an existing document.

### Are Mermaid diagrams maintained here?

Mermaid diagrams are stored under `docs/diagrams` and database folders. Do not modify generated diagrams unless diagram maintenance is explicitly requested.

## Related Documents

- [Deployment Guide](../deployment/README.md)
- [Configuration Guide](../configuration/README.md)
- [Testing Documentation](../testing/README.md)
- [Data Engineering Documentation](../data_engineering/README.md)

## Notes

Operational procedures should be rehearsed before graduation demos and before any production-like deployment.

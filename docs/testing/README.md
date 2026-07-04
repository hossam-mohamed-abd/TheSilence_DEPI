# Testing Documentation

## Overview

MediSearch testing covers frontend unit tests, backend build verification, API contract checks, database connectivity checks, and data pipeline validation.

## Purpose

This document defines the expected test strategy for maintaining confidence in application behavior, data quality, and deployment readiness.

## Contents

- Test layers
- Frontend testing
- Backend testing
- API testing
- Database and ETL testing
- Release verification checklist

## Test Layers

| Layer | Goal | Example Command or Check |
| --- | --- | --- |
| Frontend unit | Validate Angular services/components. | `npm test` in `web_app/frontend` |
| Frontend build | Validate production compilation. | `npm run build` in `web_app/frontend` |
| Backend build | Validate TypeScript and Prisma generation. | `npm run build` in `web_app/Backend` |
| API smoke | Validate deployed/local API availability. | `GET /api/health` |
| Auth flow | Validate registration, login, profile, logout. | Manual/API client flow |
| Data quality | Validate loaded data and relationships. | Row counts, required fields, foreign keys |
| ETL smoke | Validate scraper/clean/upload scripts on samples. | Source-specific Python scripts |

## Frontend Testing

Frontend tests should cover:

- Services call the correct API paths.
- Guards redirect authenticated or guest users correctly.
- Components render empty, loading, success, and error states.
- Search overlay handles no-results and paginated results.
- Favorites and notification state services update counts correctly.

## Backend Testing

Backend tests should cover:

- Auth service rejects duplicate emails and invalid passwords.
- Protected routes reject missing/invalid cookies.
- Repositories return expected pagination data.
- Pharmacy detail calculations are correct.
- Favorite toggle is idempotent for add/remove cycles.
- Notification mark-read and delete operations are scoped to the authenticated user.

## API Testing

Recommended smoke sequence:

1. `GET /api/health`
2. `GET /api/categories/home`
3. `GET /api/home/medicines/featured?page=1`
4. `GET /api/home/pharmacies?page=1`
5. `GET /api/search?q=test&page=1&limit=6`
6. Register or login.
7. `GET /api/auth/profile` with credentials.
8. Toggle a favorite.
9. Read notifications.

## Database and ETL Testing

Minimum data checks:

- No medicine rows with empty names.
- No pharmacy inventory rows without pharmacy and drug references.
- No negative prices or quantities.
- Geography hierarchy resolves from city to governorate to country.
- Favorite and inventory uniqueness constraints are preserved.
- Warehouse aggregate counts match expected operational source counts.

## Release Verification Checklist

- [ ] Frontend build passes.
- [ ] Backend build passes.
- [ ] API health endpoint returns success.
- [ ] Login/profile/logout works with cookies.
- [ ] Search returns valid response shape.
- [ ] Pharmacy details page loads inventory and categories.
- [ ] Data import row counts are recorded.
- [ ] Known issues are documented in release notes.

## Related Documents

- [Development Guide](../development/README.md)
- [API Reference](../api/API_REFERENCE.md)
- [Operations Guide](../operations/README.md)
- [Release Documentation](../release/README.md)

## Notes

Automated coverage should be expanded around the current API modules before production use. Manual graduation-demo checks should follow the release verification checklist.

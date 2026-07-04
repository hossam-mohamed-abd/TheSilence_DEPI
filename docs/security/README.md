# Security Documentation

## Overview

MediSearch uses browser-based authentication, an Express API, a PostgreSQL database accessed through Prisma, and a data pipeline that imports pharmacy and medicine data from external sources.

## Purpose

This document defines the security expectations for authentication, authorization, data protection, secrets, API hardening, and operational review.

## Contents

- Authentication and session security
- Authorization boundaries
- Data protection and privacy
- API and CORS controls
- Dependency and pipeline risks
- Security checklist

## Authentication

- Users register and log in with email and password.
- Passwords are hashed with bcrypt before storage.
- Login and registration issue a JWT in an HTTP-only `token` cookie.
- The auth middleware reads the cookie, verifies the JWT, and attaches the user identifier to the request.
- Logout clears the cookie.

## Authorization

Implemented protected resources:

- Favorites require an authenticated user.
- Notifications require an authenticated user.
- Adding pharmacy reviews requires an authenticated user.
- Profile retrieval requires an authenticated user.

Recommended production additions:

- Add role-based middleware for administrative geography creation routes.
- Add ownership checks for pharmacy staff and inventory-management workflows before enabling write operations.
- Add rate limits to login, registration, search, review creation, and upload endpoints.

## Data Protection

Sensitive data includes:

- User names, email addresses, phone numbers, profile images, and city references.
- Password hashes.
- JWT signing secrets.
- Database connection strings.
- Pharmacy contact data and inventory data.

Controls:

- Store secrets only in environment variables or platform secret managers.
- Never commit `.env` files containing real credentials.
- Use HTTPS in production.
- Use least-privilege database users for application and ETL workloads.
- Avoid logging request bodies containing passwords or tokens.

## API Hardening

Current API protections include Helmet security headers, JSON body parsing, cookie parsing, CORS allow-listing, and JWT cookie verification for protected routes.

Production recommendations:

- Enforce strict origin configuration per environment.
- Validate all request bodies consistently with schema validation.
- Normalize error messages to avoid leaking internal details.
- Add request-size limits for JSON and upload endpoints.
- Add audit logging for privileged actions and data imports.

## Pipeline and Scraping Security

- Treat scraped data as untrusted input.
- Sanitize names, descriptions, URLs, and prices before loading.
- Store raw data separately from cleaned staging outputs.
- Validate required fields before upload to operational tables.
- Track source, scrape date, and transformation version where possible.

## Security Checklist

- [ ] `DATABASE_URL` is stored in a secret manager.
- [ ] JWT secret is strong and rotated as needed.
- [ ] Production cookies are `secure` and compatible with the deployed frontend domain.
- [ ] Administrative write endpoints are protected by role checks.
- [ ] Dependency scans are run before release.
- [ ] Database backups and restore tests are scheduled.
- [ ] Scraping jobs have source-specific throttling and error handling.

## Related Documents

- [API Reference](../api/API_REFERENCE.md)
- [Backend Documentation](../backend/README.md)
- [Deployment Guide](../deployment/README.md)
- [Configuration Guide](../configuration/README.md)

## Notes

Security controls should be reviewed before each production deployment and after any authentication, database, or pipeline change.

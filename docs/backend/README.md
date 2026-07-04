# Backend Documentation

## Overview

The MediSearch backend is an Express 5 and TypeScript REST API backed by PostgreSQL through Prisma. It provides authentication, medicine discovery, pharmacy details, favorites, notifications, search, geography lookup, and home-page statistics.

## Purpose

This document describes the implemented backend structure so developers can maintain API modules, extend business logic, troubleshoot database access, and keep frontend contracts stable.

## Contents

- Runtime and dependencies
- Project structure
- Request lifecycle
- Module responsibilities
- Authentication and cookies
- Database layer
- Error handling
- Related documents

## Runtime and Dependencies

- Node.js backend using TypeScript.
- Express for HTTP routing.
- Prisma Client for PostgreSQL access.
- bcrypt for password hashing.
- jsonwebtoken for JWT creation and verification.
- cookie-parser for reading authentication cookies.
- cors and helmet for browser integration and security headers.
- zod is available for validation, although not all controllers currently enforce schema validation.

## Project Structure

| Path | Responsibility |
| --- | --- |
| `web_app/Backend/src/app.ts` | Creates the Express app, configures middleware, health checks, CORS, and route mounting. |
| `web_app/Backend/src/server.ts` | Starts the HTTP server. |
| `web_app/Backend/src/config/prisma.ts` | Exposes Prisma Client configuration. |
| `web_app/Backend/src/middleware/auth.middleware.ts` | Validates the HTTP-only JWT cookie and attaches the user ID to the request. |
| `web_app/Backend/src/modules/*/*.routes.ts` | Defines endpoint paths for each domain module. |
| `web_app/Backend/src/modules/*/*.controller.ts` | Handles HTTP request/response concerns. |
| `web_app/Backend/src/modules/*/*.service.ts` | Contains business logic. |
| `web_app/Backend/src/modules/*/*.repository.ts` | Encapsulates Prisma queries. |
| `web_app/Backend/prisma/schema.prisma` | Defines the PostgreSQL schema used by Prisma Client. |

## Request Lifecycle

1. Express receives the request.
2. Helmet applies baseline security headers.
3. CORS validates browser origin and credential policy.
4. JSON body parsing and cookie parsing run.
5. The mounted route delegates to a controller.
6. Protected routes run `authMiddleware` before controller logic.
7. Controllers call services.
8. Services call repositories.
9. Repositories query PostgreSQL through Prisma.
10. Controllers return JSON responses, serializing BigInt values where needed.

## Module Responsibilities

| Module | Responsibilities |
| --- | --- |
| `auth` | Register, login, profile, logout, bcrypt password hashing, JWT issuance, welcome notification creation. |
| `categories` | Home-page category retrieval. |
| `medicines` | Featured medicine retrieval for the home page. |
| `pharmacies` | Featured pharmacies, pharmacy details, inventory filters, categories, reviews, pharmacy statistics. |
| `favorites` | Authenticated favorite toggle, favorite list, and favorite count. |
| `notifications` | Authenticated notification list, unread count, mark-read, delete, and welcome notification creation. |
| `search` | Query-based medicine and inventory search with pagination. |
| `statistics` | Aggregate metrics for the home page. |
| `countries`, `governorates`, `cities` | Geography lookup and basic creation endpoints. |

## Authentication and Cookies

- The backend issues a JWT in an HTTP-only cookie named `token`.
- Local cookies use `sameSite: lax`.
- Production login cookies use `sameSite: none` and `secure: true` when `NODE_ENV=production`.
- Frontend protected calls must set `withCredentials: true`.
- Missing cookies return `401 Unauthorized`; invalid cookies return `401 Invalid Token`.

## Database Layer

Prisma models include users, geography, drugs, drug categories, alternatives, tags, pharmacies, inventory, pharmacy staff, ratings, favorites, notifications, alerts, search logs, price history, availability history, and drug analytics.

Important relationship groups:

- `countries` -> `governorates` -> `cities` -> `users` and `pharmacies`.
- `drug_categories` -> `drugs` -> `pharmacy_inventory`.
- `users` -> `favorites`, `notifications`, `pharmacy_ratings`, and `search_logs`.
- `pharmacies` -> `pharmacy_inventory`, `pharmacy_ratings`, `pharmacy_staff`, and `alerts`.

## Error Handling

Current controllers use local `try/catch` blocks and return module-specific status codes:

- Authentication errors generally return `400` or `404`.
- Protected-route failures return `401` from middleware.
- Missing pharmacy details return `404`.
- Most query or persistence failures return `500`.

Recommended improvements:

- Add centralized error middleware.
- Standardize validation errors.
- Replace internal error messages with safe public messages for production.
- Add structured logging with request IDs.

## Related Documents

- [API Reference](../api/API_REFERENCE.md)
- [Database Documentation](../database/README.md)
- [Security Documentation](../security/README.md)
- [Development Guide](../development/README.md)

## Notes

Keep controllers thin. New backend features should follow the existing route-controller-service-repository pattern and update API documentation in the same change.

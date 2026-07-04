# API Reference

## Overview

MediSearch exposes a REST API from the Express backend under the `/api` prefix. The API supports authentication, home-page data, pharmacy detail pages, medicine search, favorites, notifications, and geography lookup.

## Purpose

This reference helps frontend developers, backend maintainers, QA engineers, and integrators understand the implemented endpoints, authentication requirements, query parameters, and response conventions.

## Contents

- Base URL and health checks
- Authentication and cookie behavior
- Endpoint catalog
- Response and error conventions
- Related implementation notes

## Base URL

| Environment | URL |
| --- | --- |
| Local API | `http://localhost:3000/api` |
| Local root health | `http://localhost:3000/` and `http://localhost:3000/api/health` |
| Frontend local consumer | `http://localhost:4200` |

The Angular frontend reads the API base URL from `environment.apiUrl`.

## Authentication Model

Authentication uses a JWT stored in an HTTP-only cookie named `token`.

- `POST /api/auth/register` and `POST /api/auth/login` set the cookie.
- Protected endpoints require the cookie to be sent with `withCredentials: true` from the browser.
- `POST /api/auth/logout` clears the cookie.
- The backend middleware rejects missing or invalid cookies with `401` responses.

## Response Conventions

Most endpoints return JSON with a `success` boolean. Data-bearing endpoints usually return `data`, `user`, `count`, pagination metadata, or module-specific fields.

Common error format:

```json
{
  "success": false,
  "message": "Error details"
}
```

BigInt identifiers are serialized as strings unless a service explicitly converts them to numbers.

## Endpoint Catalog

### System

| Method | Path | Auth | Purpose |
| --- | --- | --- | --- |
| `GET` | `/` | No | Confirms that the API process is running. |
| `GET` | `/api/health` | No | Health-check endpoint for deployment monitoring. |

### Authentication

| Method | Path | Auth | Purpose |
| --- | --- | --- | --- |
| `POST` | `/api/auth/register` | No | Creates a customer account, hashes the password, creates a welcome notification, and sets the JWT cookie. |
| `POST` | `/api/auth/login` | No | Validates credentials and sets the JWT cookie. |
| `GET` | `/api/auth/profile` | Yes | Returns the authenticated user profile. |
| `POST` | `/api/auth/logout` | No | Clears the JWT cookie. |

Register payload:

```json
{
  "firstName": "Aya",
  "lastName": "Hassan",
  "email": "aya@example.com",
  "password": "StrongPassword123",
  "phone": "+201000000000",
  "cityId": 1
}
```

Login payload:

```json
{
  "email": "aya@example.com",
  "password": "StrongPassword123"
}
```

### Geography

| Method | Path | Auth | Purpose |
| --- | --- | --- | --- |
| `GET` | `/api/countries` | No | Lists countries. |
| `GET` | `/api/governorates/:countryId` | No | Lists governorates for a country. |
| `POST` | `/api/governorates` | No | Creates a governorate from `name` and `countryId`. |
| `GET` | `/api/cities/:governorateId` | No | Lists cities for a governorate. |
| `POST` | `/api/cities` | No | Creates a city from `name` and `governorateId`. |

### Home Page

| Method | Path | Auth | Purpose |
| --- | --- | --- | --- |
| `GET` | `/api/categories/home` | No | Returns home-page drug categories plus total and remaining count. |
| `GET` | `/api/home/medicines/featured?page=1` | No | Returns paginated featured medicines. |
| `GET` | `/api/home/pharmacies?page=1` | No | Returns paginated featured pharmacies. |
| `GET` | `/api/home/statistics` | No | Returns aggregate statistics for the home page. |

### Pharmacy Details

| Method | Path | Auth | Purpose |
| --- | --- | --- | --- |
| `GET` | `/api/home/pharmacies/:id` | No | Returns a pharmacy summary including address, contact, rating, counts, and location. |
| `GET` | `/api/home/pharmacies/:id/medicines` | No | Returns pharmacy inventory medicines. Supports filters and pagination. |
| `GET` | `/api/home/pharmacies/:id/categories` | No | Returns categories available in that pharmacy inventory. |
| `GET` | `/api/home/pharmacies/:id/reviews?page=1` | No | Returns paginated pharmacy reviews. |
| `POST` | `/api/home/pharmacies/:id/reviews` | Yes | Adds or updates an authenticated user's pharmacy review. |
| `GET` | `/api/home/pharmacies/:id/statistics` | No | Returns pharmacy-specific inventory/statistics data. |

Medicine inventory query parameters:

| Parameter | Default | Description |
| --- | --- | --- |
| `page` | `1` | Page number. |
| `limit` | `12` | Page size. |
| `search` | empty | Text filter for medicines. |
| `category` | none | Drug category ID. |
| `available` | `false` | When `true`, returns in-stock items only. |
| `sort` | `name_asc` | Backend-supported sort key. |

Review payload:

```json
{
  "rating": 5,
  "review": "Helpful pharmacy and clear stock information."
}
```

### Search

| Method | Path | Auth | Purpose |
| --- | --- | --- | --- |
| `GET` | `/api/search?q=panadol&page=1&limit=12` | No | Searches medicines and related inventory results. |

### Favorites

All favorites endpoints require authentication.

| Method | Path | Purpose |
| --- | --- | --- |
| `POST` | `/api/favorites` | Toggles a favorite medicine for the authenticated user. |
| `GET` | `/api/favorites` | Returns the authenticated user's saved medicines. |
| `GET` | `/api/favorites/count` | Returns the user's favorite count. |

Toggle payload:

```json
{
  "drugId": 10
}
```

### Notifications

All notification endpoints require authentication.

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/api/notifications` | Lists notifications for the authenticated user. |
| `GET` | `/api/notifications/unread-count` | Counts unread notifications. |
| `PATCH` | `/api/notifications/read-all` | Marks all notifications as read. |
| `PATCH` | `/api/notifications/:id/read` | Marks one notification as read. |
| `DELETE` | `/api/notifications` | Deletes all notifications for the user. |
| `DELETE` | `/api/notifications/:id` | Deletes one notification. |

## Related Documents

- [Backend Documentation](../backend/README.md)
- [Frontend Documentation](../frontend/README.md)
- [Security Guide](../security/README.md)
- [Database Documentation](../database/README.md)

## Notes

- Some geography creation routes are currently unauthenticated; production hardening should restrict them to administrative roles.
- Keep this reference synchronized with `web_app/Backend/src/app.ts` and module route files whenever endpoints change.

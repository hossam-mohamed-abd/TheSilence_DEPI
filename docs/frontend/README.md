# Frontend Documentation

## Overview

The MediSearch frontend is an Angular application that presents medicine search, featured medicines, pharmacy discovery, pharmacy detail pages, authentication pages, favorites, notifications, and user-facing informational sections.

## Purpose

This document describes the implemented Angular structure, routing, shared modules, services, state management, and API integration points.

## Contents

- Runtime and framework
- Application structure
- Routing
- Components and pages
- Services and models
- State management
- UI architecture
- Related documents

## Runtime and Framework

- Angular 21 application.
- TypeScript and RxJS.
- Angular Router for client-side navigation.
- Angular `HttpClient` for API calls.
- Angular signals for lightweight favorites and notification state.
- Browser local storage for persisted user state.

## Application Structure

| Path | Responsibility |
| --- | --- |
| `web_app/frontend/src/app/app.routes.ts` | Top-level route declarations. |
| `web_app/frontend/src/app/components` | Main pages and reusable visual components. |
| `web_app/frontend/src/app/components/home` | Home page composition and home section components. |
| `web_app/frontend/src/app/components/shared` | Navbar, footer, search overlay, drug card, auth-required modal. |
| `web_app/frontend/src/app/features/auth` | Login and register pages plus auth routing/module files. |
| `web_app/frontend/src/app/core/services` | API clients, state services, guards, and UI helper services. |
| `web_app/frontend/src/app/core/models` | TypeScript models for API contracts. |
| `web_app/frontend/src/environments` | Local and production API URL configuration. |

## Routing

| Route | Component | Notes |
| --- | --- | --- |
| `/` | `HomeComponent` | Main landing and discovery page. |
| `/login` | `Login` | Guarded by guest guard so authenticated users are redirected home. |
| `/register` | `RegisterComponent` | Guarded by guest guard. |
| `/pharmacies/:id` | Lazy-loaded `PharmacyDetailsComponent` | Loads pharmacy profile, inventory, categories, and reviews. |
| `**` | Redirect to `/` | Fallback route. |

## Components and Pages

### Home Page Sections

- Hero/search entry point.
- Popular searches.
- Categories.
- Featured medicines.
- Featured pharmacies.
- Statistics.
- AI features marketing section.

### Shared Components

- Navbar with authentication-aware UI, favorites indicator, and notifications.
- Footer.
- Search overlay for medicine search results.
- Drug card for displaying medicine/inventory details and favorite controls.
- Auth-required modal for actions that require login.

### Pharmacy Details

The pharmacy detail page displays pharmacy identity, location/contact data, ratings, inventory filters, category filters, medicine cards, reviews, and supporting statistics.

## Services and Models

| Service | API Area |
| --- | --- |
| `AuthService` | Login, register, profile, logout, countries, governorates, and cities. |
| `CategoryService` | Home categories. |
| `MedicineService` | Featured medicines. |
| `PharmacyService` | Featured pharmacies, pharmacy details, medicines, categories, reviews. |
| `SearchService` | Query search. |
| `FavoriteService` | Favorite toggle, list, and count. |
| `NotificationService` | Notifications and read/delete actions. |
| `StatisticsService` | Home statistics. |
| `FavoriteFlyService` | Favorite animation helper. |

Models under `core/models` describe users, login/register requests, drugs, pharmacies, categories, notifications, and home category responses.

## State Management

The application uses lightweight local state rather than a full global store:

- `AuthStateService` uses a `BehaviorSubject` and local storage key `ms_user`.
- `FavoriteStateService` uses Angular signals for favorite list and count.
- `NotificationStateService` uses Angular signals and a computed unread count.

## UI Architecture

- Feature pages compose smaller presentational components.
- API access stays in services instead of components.
- Shared components keep navigation, modal, search, card, and layout behavior consistent.
- Environment files isolate API base URL selection.

## Related Documents

- [API Reference](../api/API_REFERENCE.md)
- [Backend Documentation](../backend/README.md)
- [Development Guide](../development/README.md)
- [Testing Documentation](../testing/README.md)

## Notes

When frontend API usage changes, update this document and the API reference together so route paths, credential behavior, and response expectations remain aligned.

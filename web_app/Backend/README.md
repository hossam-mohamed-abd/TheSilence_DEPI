# MediSearch Backend Application

## Overview

The MediSearch Backend Application is the server-side component of the MediSearch platform.

It is responsible for:

- Business Logic
- Authentication & Authorization
- Drug Search APIs
- Price Comparison APIs
- Pharmacy Management
- User Management
- Recommendation Services Integration
- Communication with Databases and Data Pipelines

The backend follows a RESTful API architecture and is deployed using serverless infrastructure on Vercel. Vercel supports backend deployments through serverless functions and Node.js runtimes. :contentReference[oaicite:0]{index=0}

---

# Live API

Production URL:

https://medi-search-backend.vercel.app/

Hosting Platform:

Vercel

---

# Source Code Repository

Repository:

https://github.com/hossam-mohamed-abd/MediSearch_backend.git

---

# Technology Stack

## Runtime

- Node.js

## Framework

- Express.js

## Language

- JavaScript

## Authentication

- JWT
- Cookies

## Database

- PostgreSQL (Neon)

## Storage

- Supabase Storage
- Backblaze B2

## Deployment

- Vercel

---

# System Responsibilities

The backend is responsible for:

- API Endpoints
- Authentication
- Authorization
- Business Logic
- Database Access
- File Processing Integration
- Recommendation Integration
- Notifications
- Search APIs

---

# Supported Roles

## Patient

Features:

- Search drugs
- Compare prices
- Manage favorites
- Receive notifications

---

## Pharmacy

Features:

- Manage inventory
- Upload inventory files
- Update stock
- Update prices

---

## Admin

Features:

- Manage users
- Manage pharmacies
- Manage drugs
- Monitor system analytics

---

# High-Level Architecture

```text
Frontend (Angular)
        ↓
REST APIs
        ↓
Backend (Express.js)
        ↓
Main Database (PostgreSQL)
        ↓
Data Pipelines
        ↓
Warehouse & Analytics
```

---

# Expected Integrations

## Main Database

- PostgreSQL (Neon)

## Landing Zone

- Supabase Storage

## Raw Data Lake

- Backblaze B2

## AI Services

- Recommendation Engine
- Similarity Models
- Search Engine

---

# Suggested Project Structure

```text
src
│
├── config
│
├── controllers
│
├── middleware
│
├── models
│
├── routes
│
├── services
│
├── utils
│
├── validations
│
└── app.js
```

---

# Main Modules

## Authentication Module

Responsibilities:

- Register
- Login
- Logout
- Refresh Token
- Role Management

---

## Drug Module

Responsibilities:

- Drug Search
- Drug Details
- Drug Alternatives
- Price Comparison

---

## Pharmacy Module

Responsibilities:

- Inventory Management
- Price Management
- Stock Updates

---

## User Module

Responsibilities:

- Favorites
- Notifications
- Search History
- Profile Management

---

# API Categories

```text
/api/auth
/api/users
/api/drugs
/api/pharmacies
/api/favorites
/api/notifications
/api/search
/api/recommendations
```

---

# Environment Variables

```env
PORT=

DATABASE_URL=

JWT_SECRET=

JWT_EXPIRES_IN=

REFRESH_TOKEN_SECRET=

SUPABASE_URL=
SUPABASE_KEY=

B2_ENDPOINT=
B2_KEY_ID=
B2_APPLICATION_KEY=

FRONTEND_URL=
```

---

# Installation

```bash
git clone https://github.com/hossam-mohamed-abd/MediSearch_backend.git

cd MediSearch_backend

npm install
```

---

# Run Development Server

```bash
npm run dev
```

---

# Run Production

```bash
npm start
```

---

# Deployment

Production API:

https://medi-search-backend.vercel.app/

Source Code:

https://github.com/hossam-mohamed-abd/MediSearch_backend.git

Vercel provides serverless backend support for Node.js and Express applications and automatically deploys changes from Git repositories. :contentReference[oaicite:1]{index=1}

---

# Responsibilities Outside Backend Scope

The backend does NOT handle:

- Data Cleaning
- ETL Pipelines
- Warehouse Processing
- Machine Learning Training
- Analytics Processing

These responsibilities belong to the Data Engineering layer.

---

# Architecture Integration

```text
Angular Frontend
        ↓
Backend APIs
        ↓
PostgreSQL
        ↓
Landing Zone
        ↓
Data Pipelines
        ↓
Data Warehouse
        ↓
Analytics & AI
```

---

# Status

```text
Current Stage:
MVP Development
```

```text
Deployment:
Production API Available
```

```text
Repository:
Public GitHub Repository
```

---

# Quick Links

| Resource | URL |
|----------|-----|
| Frontend | https://medi-search-eight.vercel.app/ |
| Backend API | https://medi-search-backend.vercel.app/ |
| Frontend Repository | https://github.com/hossam-mohamed-abd/MediSearch |
| Backend Repository | https://github.com/hossam-mohamed-abd/MediSearch_backend.git |
| UI/UX Design | https://www.figma.com/board/qygMtKJHuPAP0KwOt1JauR/MediSearch |

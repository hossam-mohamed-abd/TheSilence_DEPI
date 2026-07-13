# Database Configuration Guide

## DEBI Project - Neon PostgreSQL

This document explains how to connect to the project's PostgreSQL database hosted on Neon and use it in development, deployment pipelines, and production environments.

---

# Database Provider

- Provider: Neon
- Database Engine: PostgreSQL
- Default Port: `5432`
- SSL: Required

---

# Connection Information

## Host

```env
DB_HOST=
```

## Database

```env
DB_NAME=neondb
```

## User

```env
DB_USER=neondb_owner
```

## Port

```env
DB_PORT=5432
```

## Endpoint ID

```env
DB_ENDPOINT=
```

---

# PHP Connection Example

```php
<?php

$host = getenv('DB_HOST');
$dbname = getenv('DB_NAME');
$user = getenv('DB_USER');
$password = getenv('DB_PASSWORD');
$endpoint = getenv('DB_ENDPOINT');

$conn = pg_connect(
    "host=$host
    port=5432
    dbname=$dbname
    user=$user
    password=$password
    sslmode=require
    options='endpoint=$endpoint'"
);

if (!$conn) {
    die('Database Connection Failed');
}

echo "Connected Successfully";
```

---

# Environment Variables (.env)

```env
DB_CONNECTION=pgsql
DB_HOST=
DB_PORT=5432
DB_DATABASE=neondb
DB_USERNAME=neondb_owner
DB_PASSWORD=YOUR_DATABASE_PASSWORD
DB_ENDPOINT=
DB_SSLMODE=require
```

---

# Docker Example

```yaml
environment:
  DB_CONNECTION: pgsql
  DB_HOST: ep-spring-sound-atfc1f55-pooler.c-9.us-east-1.aws.neon.tech
  DB_PORT: 5432
  DB_DATABASE: neondb
  DB_USERNAME: neondb_owner
  DB_PASSWORD: ${DB_PASSWORD}
  DB_ENDPOINT: ep-spring-sound-atfc1f55
```

---

# GitHub Actions Example

```yaml
env:
  DB_CONNECTION: pgsql
  DB_HOST: ep-spring-sound-atfc1f55-pooler.c-9.us-east-1.aws.neon.tech
  DB_PORT: 5432
  DB_DATABASE: neondb
  DB_USERNAME: neondb_owner
  DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
  DB_ENDPOINT: ep-spring-sound-atfc1f55
```

---

# Laravel Configuration

```env
DB_CONNECTION=pgsql
DB_HOST=ep-spring-sound-atfc1f55-pooler.c-9.us-east-1.aws.neon.tech
DB_PORT=5432
DB_DATABASE=neondb
DB_USERNAME=neondb_owner
DB_PASSWORD=YOUR_DATABASE_PASSWORD
DB_SSLMODE=require
```

---

# Node.js Example

```javascript
const { Pool } = require("pg");

const pool = new Pool({
  host: process.env.DB_HOST,
  port: 5432,
  database: process.env.DB_DATABASE,
  user: process.env.DB_USERNAME,
  password: process.env.DB_PASSWORD,
  ssl: {
    rejectUnauthorized: false,
  },
});

module.exports = pool;
```

---

# Connection String

```text
postgresql://neondb_owner:<PASSWORD>@ep-spring-sound-atfc1f55-pooler.c-9.us-east-1.aws.neon.tech/neondb?sslmode=require
```

---

# Security Recommendations

- Never commit database passwords to Git.
- Store credentials in environment variables.
- Store production passwords in CI/CD secrets.
- Rotate credentials periodically.
- Grant least-privilege permissions to application users.

---

# CI/CD Pipeline Checklist

- [ ] Add database password to Secrets Manager.
- [ ] Configure environment variables.
- [ ] Run database migrations.
- [ ] Verify SSL is enabled.
- [ ] Run health checks after deployment.
- [ ] Validate database connectivity before starting the application.

---

# Connectivity Test Query

```sql
SELECT version();
```

---

# List Tables

```sql
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;
```

---

# Health Check Query

```sql
SELECT NOW();
```

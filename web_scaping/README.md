
# Web Scraping Module

## Overview

This folder contains all web scraping source code used in the MediSearch project.

Its purpose is to collect data from pharmacy websites and external sources and prepare it for the Data Engineering pipelines.

This folder contains **source code only** and must never contain datasets or generated files.

---

# Folder Structure

Each pharmacy should have its own folder.

Example:

```text
web_scraping/
│
├── el_ezaby/
│   ├── scraper.py
│   ├── parser.py
│   ├── urls.py
│   └── config.py
│
├── seif/
│   ├── scraper.py
│   ├── parser.py
│   └── config.py
│
└── rushdy/
    ├── scraper.py
    └── config.py
```

---

# Responsibilities

The scraping modules are responsible for:

- Collecting drug information
- Collecting prices
- Collecting availability
- Collecting categories
- Exporting raw data to the Data Lake

---

# Data Destination

Scraped data should be uploaded to:

```text
Raw Data Lake (Backblaze B2)
```

or

```text
Pharmacy Landing Zone
```

depending on the pipeline requirements.

---

# Rules

✅ Store source code only.

✅ One folder per pharmacy.

✅ Keep reusable utilities separated.

❌ Do not upload datasets.

❌ Do not upload CSV files.

❌ Do not upload JSON files.

❌ Do not upload temporary files.

❌ Do not upload notebooks.

---

# Recommended Structure

```text
pharmacy_name/
│
├── scraper.py
├── parser.py
├── config.py
├── urls.py
└── utils.py
```

---

# Technologies

- Python
- Requests
- BeautifulSoup
- Selenium
- Playwright
- Pandas

---

# Workflow

```text
Pharmacy Website
        ↓
Web Scraper
        ↓
Raw Data
        ↓
Data Lake
        ↓
ETL Pipelines
```

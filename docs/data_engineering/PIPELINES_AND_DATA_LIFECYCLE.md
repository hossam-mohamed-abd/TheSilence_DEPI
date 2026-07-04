# Pipelines and Data Lifecycle

## Overview

MediSearch data engineering moves medicine, pharmacy, category, geography, pricing, and inventory data from external sources into raw storage, staging outputs, operational PostgreSQL tables, and analytical warehouse structures.

## Purpose

This document explains how data should flow through the project and how engineers should validate, load, monitor, and maintain data assets.

## Contents

- Data lifecycle stages
- Scraping sources
- Cleaning and transformation
- Upload workflow
- Warehouse and analytics workflow
- Data quality checks

## Data Lifecycle Stages

| Stage | Location | Description |
| --- | --- | --- |
| Raw | `data/raw`, source scraper outputs | Original collected data with minimal modification. |
| Staging | `data/staging`, cleaning outputs | Normalized, deduplicated, type-corrected data ready for loading. |
| Operational database | PostgreSQL main database | Application tables used by backend APIs. |
| Warehouse | `data/warehouse` and warehouse database assets | Analytical fact/dimension structures for reporting. |
| Analytics | `analytics` | Reports, notebooks, model outputs, and insights. |

## Scraping Sources

Scrapers under `web_scaping` target pharmacy and medicine data sources, including Gardenia, aldawaaegy, Bloom pharmacy scripts, FDA notebook work, and category-specific scraping scripts for medications, vitamins, skin care, hair care, mom/baby, devices, makeup accessories, sexual wellness, and daily essentials.

Expected raw fields include source product name, category, price, availability, images, descriptions, pharmacy/source name, and timestamps where possible.

## Cleaning and Transformation

Cleaning scripts under `pipelines/cleaning` normalize data before upload. Transformations should:

- Trim and normalize text fields.
- Standardize prices as decimals.
- Normalize availability and quantity fields.
- Deduplicate medicines and pharmacy inventory rows.
- Map countries, governorates, and cities to database IDs.
- Validate URLs for images and source references.
- Preserve source identifiers where available.

## Pharmacy Upload Workflow

1. Scrape pharmacy data into raw storage.
2. Inspect raw output for source layout changes.
3. Clean fields and create staging data.
4. Ensure geography records exist.
5. Load pharmacies.
6. Load drug categories and drugs.
7. Load pharmacy inventory with `pharmacy_id` and `drug_id` relationships.
8. Validate row counts and sample API responses.
9. Record load date, source, and known limitations.

## Warehouse and Analytics Workflow

The warehouse should consume validated operational/staging data to support:

- Drug availability trends.
- Price min/max/average analytics.
- Search and demand analysis.
- Pharmacy coverage by city/governorate.
- Category distribution and inventory health.

Warehouse loads should be repeatable, auditable, and separated from raw scraping scripts.

## Data Quality Checks

Minimum checks before loading:

- Required IDs exist and foreign keys can be resolved.
- Prices are numeric and non-negative.
- Quantity values are numeric and non-negative.
- Medicine names are not empty.
- Pharmacy names and city references are not empty.
- Duplicate inventory rows are resolved against the unique pharmacy/drug relationship.
- Sample API calls return expected records after loading.

## Related Documents

- [Data Engineering README](README.md)
- [Warehouse Documentation](warehouse/README.md)
- [Database Documentation](../database/README.md)
- [Operations Guide](../operations/README.md)

## Notes

Keep raw data immutable. If a transformation changes, regenerate staging outputs from raw data rather than editing raw files directly.

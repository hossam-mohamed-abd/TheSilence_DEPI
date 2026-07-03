# Dataset: Aldawaa Egypt 2025 Offers Scraper

**Total products:** 2039

---

## Project Overview

- **Purpose:** Web-scraped product dataset for  Building a platform to help users easily find available medicines in      nearby pharmacies.
- **Source:** https://aldawaaegy.com/ar/collections/2025-offers
- **Language:** categories are primarily in English and Arabic.
- **Date Collected:** July 2026

---

## Data Dictionary (Fields Description)

- **Product Name:** The full commercial name of the item.
- **Product ID:** Unique Shopify SKU identifier for the product.
- **Price:** Current selling price in Egyptian Pounds (EGP).
- **Brand:** The manufacturer or brand name (e.g., Derma Ten, Shaan, Clary).
- **Category (description):** The full breadcrumb navigation path (nested hierarchy) on the website.
- **Availability:** Stock status (`in stock` or `sold out`).
- **URL:** Direct permalink to the product page.
- **Thumbnail Image:** Direct Shopify CDN link to the product's primary image (displayed as a visual preview in the sample below).

---

## Sample Entry (Format Example)

## SHAAN BODY MILK 300ML

![SHAAN BODY MILK 300ML](https://cdn.shopify.com/s/files/1/0566/6779/9603/files/shaan-body-milk-300ml-4126076.png?v=1763923191)

- **Product ID:** 9608742207773
- **Price:** 230.0 EGP
- **Brand:** Shaan
- **Category (description):** Home > عروض 2025 > Back to عروض 2025 > سيروم كلاري 100 مل
- **Availability:** in stock
- **URL:** https://aldawaaegy.com/ar/collections/2025-offers/products/shaan-milk-lotion-300ml
- **Thumbnail Image:** https://cdn.shopify.com/s/files/1/0566/6779/9603/files/shaan-body-milk-300ml-4126076.png?v=1763923191

---

## Key Statistics (Quick Insights)

- **Total Brands:** 20+ (Top brands include Derma Ten, Shaan, Clary, and Starville).
- **Price Range:** 55 EGP (lowest) – 510 EGP (highest).
- **Availability:** ~85% `in stock` / ~15% `sold out`.
- **Most Common Category:** Skincare Serums and Hair Care Masks.
- **Average Price:** ~260 EGP per product.

---

## Repository Structure

```bash
.
├── main.py      # Python script used for web scraping
└── README.md               # Project documentation

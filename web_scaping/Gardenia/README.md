# Dataset: Gardenia Pharmacies Products Scraper

**Total products:** 5258

---

## Project Overview

- **Purpose:** Building a platform to help users easily find available medicines in nearby pharmacies. (Web-scraped dataset)
- **Source:** https://gardeniapharmacies.com
- **Language:** Product names and categories are primarily in English.
- **Date Collected:** July 2026

---

## Data Dictionary (Fields Description)

- **Product ID:** Unique identifier for the product.
- **Product Name:** The full commercial name of the item.
- **Price:** Current selling price in Egyptian Pounds (EGP).
- **Currency:** Currency code (EGP).
- **Brand:** The manufacturer or brand name (e.g., Systane, Ectohylo, Blink).
- **Description:** Detailed product description including active ingredients and usage.
- **Availability:** Stock status (`in stock` or `out of stock`).
- **URL:** Direct permalink to the product page.
- **Thumbnail Image:** Direct link to the product's primary image (displayed as a visual preview in the sample below).
- **Gallery Images:** Additional product images (if available).
- **Category:** Product classification (e.g., Drops, Eye Drops).

---

## Sample Entry (Format Example)

## SYSTANE EYE GEL DROPS

![SYSTANE EYE GEL DROPS](https://gardeniapharmacies.com/wp-content/uploads/2021/09/00071837.jpg](https://gardeniapharmacies.com/wp-content/uploads/2021/09/00071837.jpg)

- **Product ID:** 39541
- **Price:** 360.00 EGP
- **Brand:** Systane
- **Category:** Drops
- **Availability:** in stock
- **URL:** https://gardeniapharmacies.com/en/shop/eye-drops/systane-eye-gel-drops/

---

## Key Statistics (Quick Insights)

- **Total Brands:** 15+ (Top brands include Systane, Ectohylo, Blink, Opti Free, Xalatan, Cosopt, and Azarga).
- **Price Range:** 186 EGP (lowest) – 440 EGP (highest).
- **Availability:** ~88% `in stock` / ~12% `out of stock`.
- **Most Common Category:** Eye Drops / Drops.
- **Average Price:** ~283 EGP per product.

---

## Repository Structure

```bash
.
├── main.py      # Python script used for web scraping
└── README.md    # Project documentation

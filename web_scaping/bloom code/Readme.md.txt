# Bloom Pharmacy Web Scraper

A collection of Python scripts for scraping product data (all categories) from [Bloom Pharmacy](https://www.bloompharmacy.com/).

## Overview

This project extracts product listings, categories, pricing, and descriptions from the Bloom Pharmacy Shopify storefront. It includes multiple scraper variants built at different stages of development — from a full-featured scraper to faster, lightweight versions, plus a bilingual variant.

## Files

| File | Description |
|---|---|
| `bloom_pharmacy_complete_scraper.py` | Full scraper — pulls all product categories and fields from the site. |
| `bloom_pharmacy_complete_with_descriptions.py` | Complete scraper variant that also captures full product descriptions. |
| `bloom_pharmacy_fast_with_descriptions.py` | Optimized/faster version that still includes product descriptions. |
| `bloom_pharmacy_scraper.py` | Base/original scraper script. |
| `bloom_pharmacy_scraper_fast.py` | Speed-optimized scraper (reduced fields/requests for quicker runs). |
| `bloom_shopify_scraper.py` | Scraper targeting the Shopify backend/API endpoints directly (e.g. `/products.json`) rather than parsing rendered HTML. |
| `convert.py` | Utility script to convert/reformat scraped output (e.g. JSON → CSV/Excel). |
| `run_scraper.sh` | Shell script to run the scraper pipeline end-to-end. |

## Output & Data

| File/Folder | Description |
|---|---|
| `bloom_pharmacy_data/` | Folder containing the scraped output data. |
| `scraper_output.txt` | Log/output from a scraper run. |
| `scraper_fast.txt` | Log/output from the fast scraper run. |
| `scraper_shopify.txt` | Log/output from the Shopify-based scraper run. |
| `scraper_shopify_v2.txt` | Log/output from a second iteration of the Shopify scraper. |
| `scraper_v3_bilingual.txt` | Log/output from the bilingual (multi-language) scraper version. |

## Categories Covered

Bloom Pharmacy's storefront is organized into categories such as (verify against the live site, as these may change):
- Weight Loss
- Sexual Health
- Skincare
- Hair Loss
- Mental Health
- General Health / Wellness

The scraper is designed to iterate through each category page, follow pagination, and collect product-level data for every listed item.

## Data Fields Collected

Depending on which scraper variant is used, fields typically include:
- Product name
- Category / subcategory
- Price
- Product URL
- Image URL(s)
- Short description
- Full description (in `*_with_descriptions` variants)
- Availability/stock status
- Language variant (in the bilingual version)

## Requirements

```bash
pip install requests beautifulsoup4 pandas
```

(Adjust based on the actual imports used in each script — e.g. `lxml`, `selenium`, or `playwright` if any script renders JavaScript.)

## Usage

Run an individual scraper directly:

```bash
python bloom_pharmacy_complete_scraper.py
```

Or run the full pipeline via the shell script:

```bash
bash run_scraper.sh
```

Convert output to another format:

```bash
python convert.py
```

## Notes

- Multiple scraper versions exist because the project evolved iteratively (base → fast → with descriptions → Shopify API-based → bilingual). Consider consolidating into a single maintained script once you confirm which version is most reliable/current.
- Respect Bloom Pharmacy's `robots.txt` and terms of service, and add reasonable request delays/rate limiting to avoid overloading their servers.
- Scraped data is for personal/research use only; verify licensing/usage rights before any commercial use.

## Suggested Folder Cleanup

Given the number of similar-named scripts, consider organizing into subfolders, e.g.:

```
bloom_pharmacy_scraper/
├── scrapers/
│   ├── complete_scraper.py
│   ├── complete_with_descriptions.py
│   ├── fast_with_descriptions.py
│   ├── scraper.py
│   ├── scraper_fast.py
│   └── shopify_scraper.py
├── utils/
│   └── convert.py
├── data/
│   └── bloom_pharmacy_data/
├── logs/
│   ├── scraper_output.txt
│   ├── scraper_fast.txt
│   ├── scraper_shopify.txt
│   ├── scraper_shopify_v2.txt
│   └── scraper_v3_bilingual.txt
├── run_scraper.sh
└── README.md
```
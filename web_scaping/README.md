# Chefaa Pharmacy Web Scraper

A robust, polite, and modular Python web scraper designed to scrape product listings and full detail pages from `chefaa.com` category-by-category.

## Directory Structure

```
chefaa_scraper/
├── data/                         # Folder containing outputs by category
│   ├── medications.csv
│   ├── medications.json
│   ├── ...
├── config.py                     # Global settings (rate limits, targets)
├── scraper_base.py               # Core scraper & HTML parsing library
├── requirements.txt              # Project package requirements
├── scrape_medications.py         # runner for medications
├── scrape_hair_care.py           # runner for hair care
├── scrape_skin_care.py           # runner for skin care
├── scrape_daily_essentials.py    # runner for daily essentials
├── scrape_mom_baby.py            # runner for mom & baby
├── scrape_makeup_accessories.py  # runner for makeup & accessories
├── scrape_health_care_devices.py # runner for medical supplies & devices
├── scrape_vitamins_supplements.py# runner for vitamins & supplements
└── scrape_sexual_wellness.py     # runner for sexual wellness
```

## Features

- **Category-by-category scraping**: Each main category has its own Python script.
- **Thorough details**: Extracts full details including `product_id`, `name`, `price`, `currency`, `brand`, `category hierarchy`, `availability` (stock status), `url`, `thumbnail_image`, `gallery_images` (image list), `description`, and `specifications`.
- **Double formats**: Generates both `.csv` and `.json` in the `data/` directory.
- **Incremental resume**: If a scraper is stopped or crashes, rerunning it will automatically read the existing output CSV file, detect already processed items by `product_id`, and skip fetching detail pages for those items (only crawling new products).
- **Polite rate limiting**: Simulates real browser requests with clean headers and requests delay (`1.5s` by default, configurable in `config.py`) to respect server load.

## Installation

Make sure you have python 3 installed. Install the dependencies:

```bash
pip install -r requirements.txt
```

## How to Run

To scrape a specific category, run its respective script from either the workspace root or the `chefaa_scraper/` directory.

### Examples:

To scrape the **Medications** category:
```bash
python chefaa_scraper/scrape_medications.py
```

To scrape the **Vitamins & Supplements** category:
```bash
python chefaa_scraper/scrape_vitamins_supplements.py
```

To scrape the **Skin Care** category:
```bash
python chefaa_scraper/scrape_skin_care.py
```

## Outputs

All output files are saved in the `chefaa_scraper/data/` folder, named after the category (e.g., `medications.csv`, `medications.json`).

### CSV Fields:
- `product_id`: Unique identifier of the product.
- `name`: Main title of the product.
- `price`: Current price value.
- `currency`: Currency code (e.g., `EGP`).
- `brand`: Brand name of the item.
- `category`: Category path (e.g. `الأدوية > الحساسية`).
- `availability`: Stock status (e.g. `in stock`).
- `url`: Absolute link to the product page on Chefaa.
- `thumbnail_image`: Link to the main listing image.
- `gallery_images`: Semicolon-separated list of all gallery image URLs.
- `description`: Clean text of product overview.
- `specifications`: Semicolon-separated list of key-value properties.

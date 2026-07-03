"""
Gardenia Pharmacies - Product Scraper
======================================

This script scrapes product data from the Gardenia Pharmacies website.
It targets a specific category defined by the TARGET_CATEGORY variable,
or all categories if set to "all".
"""

import csv
import json
import logging
import re
import time
from dataclasses import asdict, dataclass
from typing import Optional
import os

import requests
from bs4 import BeautifulSoup

# -----------------------------------------------------------------------------
# 1. General Configuration
# -----------------------------------------------------------------------------

BASE_URL = "https://gardeniapharmacies.com"
PHARMACY_PAGE = "https://gardeniapharmacies.com/en/shop/"
OUTPUT_CSV = "gardenia_products.csv"      # Will be replaced per category
OUTPUT_JSON = "gardenia_products.json"    # Currently disabled (unused)
DELAY = 1.5                               # Delay between requests (seconds)
MAX_RETRIES = 3                           # Number of retry attempts on failure

# Set the target category. Use "all" to scrape all categories.
TARGET_CATEGORY = "Sedatives, Hypnotics"

# -----------------------------------------------------------------------------
# 2. Logging Setup
# -----------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
# 3. HTTP Headers and Session
# -----------------------------------------------------------------------------

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    ),
    "Accept-Language": "ar,en;q=0.9",
}

# Create a reusable session
session = requests.Session()
session.headers.update(HEADERS)

# -----------------------------------------------------------------------------
# 4. Product Data Class
# -----------------------------------------------------------------------------

@dataclass
class Product:
    """Represents a single product's data."""
    product_id: str = ""          # Product ID
    name: str = ""                # Product name
    price: str = ""               # Price (numeric only)
    currency: str = "EGP"         # Currency code
    brand: str = ""               # Brand name
    description: str = ""         # Product description
    availability: str = ""        # Availability status (in stock / out of stock)
    url: str = ""                 # Product page URL
    thumbnail_image: str = ""     # Thumbnail image URL
    gallery_images: str = ""      # Gallery image URLs (pipe-separated)
    category: str = ""            # Category name

# -----------------------------------------------------------------------------
# 5. HTTP Helper Functions
# -----------------------------------------------------------------------------

def get_soup(url: str) -> Optional[BeautifulSoup]:
    """
    Fetch the given URL and return a BeautifulSoup object.
    Retries on failure according to MAX_RETRIES.
    """
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = session.get(url, timeout=25)
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")
        except Exception as error:
            log.warning(f"Attempt {attempt}/{MAX_RETRIES} failed: {error}")
            time.sleep(DELAY * attempt)  # Increasing backoff
    log.error(f"Failed to fetch URL: {url}")
    return None

# -----------------------------------------------------------------------------
# 6. Fetch All Categories from the Main Shop Page
# -----------------------------------------------------------------------------

def get_categories() -> list[dict]:
    """
    Retrieve all product categories available in the store.
    Returns a list of dicts with 'name' and 'url' keys.
    """
    log.info(f"Fetching categories from: {PHARMACY_PAGE}")
    all_categories = []
    seen_urls = set()
    page_url = PHARMACY_PAGE

    # Paginate through category pages if any
    while page_url:
        soup = get_soup(page_url)
        if not soup:
            break

        # Locate category items
        for item in soup.select("li.product-category, div.product-category"):
            anchor = item.select_one("a[href]")
            if not anchor:
                continue
            href = anchor["href"]
            if href in seen_urls or "product-category" not in href:
                continue
            seen_urls.add(href)

            # Extract category name with multiple fallbacks
            name = None
            name_element = item.select_one("h2, h5, .header-title, .woocommerce-loop-category__title")
            if name_element:
                name = name_element.get_text(strip=True)
            if not name:
                img = item.select_one("img")
                if img:
                    name = img.get("alt", "").strip()
            if not name:
                name = anchor.get_text(strip=True)
            if not name:
                # Fallback: extract from URL
                name = href.split("/")[-2].replace("-", " ")

            all_categories.append({"name": name, "url": href})
            log.info(f"  Found category: {name}")

        # Next page link for categories
        next_link = soup.select_one("a.next.page-numbers")
        if next_link and next_link.get("href"):
            page_url = next_link["href"]
            time.sleep(DELAY)
        else:
            break

    log.info(f"Total categories found: {len(all_categories)}")
    return all_categories

# -----------------------------------------------------------------------------
# 7. Get Product URLs from a Category Page (with Pagination)
# -----------------------------------------------------------------------------

def get_product_urls_from_category(category_url: str) -> list[str]:
    """
    Extract all product detail page URLs from a given category.
    Handles pagination automatically.
    """
    product_urls = []
    page_url = category_url

    while page_url:
        soup = get_soup(page_url)
        if not soup:
            break

        # Extract product links from current page
        for element in soup.select("li.product:not(.product-category), div.product-small"):
            anchor = element.select_one(
                "a.woocommerce-LoopProduct-link, "
                "a.woocommerce-loop-product__link, "
                "a[href*='/shop/']"
            )
            if anchor:
                href = anchor.get("href", "")
                if href and href not in product_urls and "/shop/" in href:
                    product_urls.append(href)

        # Determine next page URL with multiple selectors (fallbacks)
        next_page_url = None

        # 1. Common 'next' class
        next_link = soup.select_one("a.next")
        if next_link and next_link.get("href"):
            next_page_url = next_link["href"]

        # 2. Text-based "التالي" or "Next"
        if not next_page_url:
            for anchor in soup.select("a"):
                text = anchor.get_text(strip=True)
                if "التالي" in text or "Next" in text:
                    next_page_url = anchor.get("href")
                    break

        # 3. Arrow symbols in page numbers
        if not next_page_url:
            for anchor in soup.select("a.page-numbers"):
                text = anchor.get_text(strip=True)
                if "→" in text or "»" in text:
                    next_page_url = anchor.get("href")
                    break

        if next_page_url:
            page_url = next_page_url
            time.sleep(DELAY)
        else:
            break

    log.info(f"  Found {len(product_urls)} products in this category")
    return product_urls

# -----------------------------------------------------------------------------
# 8. Parse Individual Product Details
# -----------------------------------------------------------------------------

def parse_product(product_url: str, category: str) -> Optional[Product]:
    """
    Scrape and parse product data from its detail page.
    Returns a Product object or None on failure.
    """
    soup = get_soup(product_url)
    if not soup:
        return None

    product = Product(url=product_url, category=category)

    # --- Extract product ID ---
    # From body class (e.g., postid-123)
    body = soup.find("body")
    if body:
        for cls in body.get("class", []):
            match = re.match(r"postid-(\d+)", cls)
            if match:
                product.product_id = match.group(1)
                break
    # Fallback: from data-product_id attribute on any button
    if not product.product_id:
        button = soup.find(attrs={"data-product_id": True})
        if button:
            product.product_id = button["data-product_id"]

    # --- Extract product name ---
    title = soup.select_one(".product_title, h1.entry-title")
    if title:
        product.name = title.get_text(strip=True)

    # --- Extract price ---
    price_element = soup.select_one(
        ".price ins .woocommerce-Price-amount bdi, "
        ".price .woocommerce-Price-amount bdi"
    )
    if price_element:
        raw_price = price_element.get_text(strip=True)
        numbers = re.findall(r"[\d,\.]+", raw_price)
        product.price = numbers[0].replace(",", "") if numbers else raw_price
        # Extract currency symbol
        currency_symbol = soup.select_one(".woocommerce-Price-currencySymbol")
        if currency_symbol:
            product.currency = currency_symbol.get_text(strip=True)

    # --- Extract availability ---
    # Handles various class variants: in-stock, instock, out-of-stock, outofstock
    product.availability = "unknown"
    stock_element = soup.select_one("p.stock")
    if stock_element:
        # Normalize classes: remove hyphens and lowercase
        classes = [c.lower().replace("-", "") for c in stock_element.get("class", [])]
        if "outofstock" in classes:
            product.availability = "out of stock"
        elif "instock" in classes:
            product.availability = "in stock"
        else:
            # Fallback: check the text itself
            text = stock_element.get_text(strip=True).lower()
            if "out" in text or "out of stock" in text:
                product.availability = "out of stock"
            elif "in stock" in text:
                product.availability = "in stock"
    else:
        # If stock element missing, check add-to-cart button
        add_to_cart = soup.select_one(".single_add_to_cart_button")
        if add_to_cart:
            classes = [c.lower() for c in add_to_cart.get("class", [])]
            product.availability = "out of stock" if "disabled" in classes else "in stock"

    # --- Extract brand from logo ---
    brand_image = soup.select_one(
        ".yith-wcbr-brands-logo img, .brand img, .woobrand img"
    )
    if brand_image:
        product.brand = brand_image.get("alt", "").strip()

    # --- Extract description ---
    # Prefer short description, then full description
    short_desc = soup.select_one(
        ".woocommerce-product-details__short-description, "
        ".product-short-description"
    )
    if short_desc:
        product.description = short_desc.get_text(" ", strip=True)
    else:
        description_tab = soup.select_one("#tab-description")
        if description_tab:
            product.description = description_tab.get_text(" ", strip=True)[:500]  # Truncate

    # --- Extract thumbnail image ---
    thumb = soup.select_one(".woocommerce-product-gallery__image a img")
    if thumb:
        product.thumbnail_image = thumb.get("data-large_image") or thumb.get("src") or ""

    # --- Extract gallery images (multiple) ---
    gallery = []
    for img in soup.select(".woocommerce-product-gallery__image img"):
        src = img.get("data-large_image") or img.get("src") or ""
        if src and "svg" not in src and src not in gallery:
            gallery.append(src)
    product.gallery_images = "|".join(gallery)  # Pipe-separated

    return product

# -----------------------------------------------------------------------------
# 9. Output Writers (CSV only, JSON disabled)
# -----------------------------------------------------------------------------

# CSV column headers
FIELDNAMES = [
    "product_id",
    "name",
    "price",
    "currency",
    "brand",
    "description",
    "availability",
    "url",
    "thumbnail_image",
    "gallery_images",
    "category",
]

def save_csv(products: list, filepath: str) -> None:
    """
    Save the product list to a CSV file at the given path.
    Uses UTF-8 with BOM for proper Arabic support.
    """
    with open(filepath, "w", newline="", encoding="utf-8-sig") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)
        writer.writeheader()
        for product in products:
            writer.writerow(asdict(product))
    log.info(f"CSV saved to {filepath} ({len(products)} rows)")

def save_json(products: list, filepath: str) -> None:
    """
    Save the product list to a JSON file (currently unused, kept for future use).
    """
    with open(filepath, "w", encoding="utf-8") as json_file:
        json.dump([asdict(product) for product in products], json_file, ensure_ascii=False, indent=2)
    log.info(f"JSON saved to {filepath}")

# -----------------------------------------------------------------------------
# 10. Utility: Sanitize Filename from Category Name
# -----------------------------------------------------------------------------

def sanitize_filename(name: str) -> str:
    """
    Convert a category name to a valid filename by removing invalid characters
    and replacing spaces with underscores.
    """
    name = re.sub(r'[^\w\s\-]', '', name)
    name = name.strip().replace(' ', '_')
    if not name:
        name = "unknown_category"
    return name

# -----------------------------------------------------------------------------
# 11. Main Execution Routine
# -----------------------------------------------------------------------------

def main() -> None:
    """
    Main orchestrator: fetches categories, processes targeted categories,
    and saves each as a separate CSV file.
    """
    # Step 1: Get all categories
    categories = get_categories()
    if not categories:
        log.error("No categories found!")
        return

    # Step 2: Select target category(ies) based on TARGET_CATEGORY
    target = TARGET_CATEGORY.strip()
    selected_categories = []

    if target.lower() == "all":
        selected_categories = categories
        log.info("Scraping all categories because TARGET_CATEGORY = 'all'")
    else:
        # Case-insensitive partial match
        for category in categories:
            if target.lower() in category["name"].lower():
                selected_categories.append(category)

        if not selected_categories:
            log.error(f"Category '{target}' not found. Please check TARGET_CATEGORY.")
            log.info("Available categories:")
            for category in categories:
                log.info(f"   - {category['name']}")
            return
        else:
            log.info(f"Found {len(selected_categories)} category(ies) matching '{target}'")

    # Step 3: Scrape each selected category and save separately
    for category in selected_categories:
        log.info(f"\n{'=' * 70}")
        log.info(f"Category: {category['name']}")
        log.info(f"{'=' * 70}")

        product_urls = get_product_urls_from_category(category["url"])
        category_products = []       # Products for this category
        seen_urls = set()            # Avoid duplicates within the same category

        for product_url in product_urls:
            if product_url in seen_urls:
                continue
            seen_urls.add(product_url)

            log.info(f"  Scraping: {product_url}")
            time.sleep(DELAY)

            product = parse_product(product_url, category=category["name"])
            if product:
                category_products.append(product)
                log.info(
                    f"    OK: {product.name[:35]:35} "
                    f"Price={product.price}  Availability={product.availability}"
                )

        # Save CSV only for this category (JSON disabled)
        if category_products:
            safe_name = sanitize_filename(category["name"])
            csv_path = f"{safe_name}.csv"
            save_csv(category_products, csv_path)
        else:
            log.warning(f"No products found for category '{category['name']}'")

    log.info("\nScraping completed. All categories saved as CSV files.")

# -----------------------------------------------------------------------------
# 12. Entry Point
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    main()

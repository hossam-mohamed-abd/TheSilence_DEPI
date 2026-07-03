"""
Al Dawaa Pharmacies (Shopify) Product Scraper

This script extracts product data from a specified collection on aldawaaegy.com.
It uses Shopify's official product endpoint (/products/<handle>.js) for core data
and optionally fetches the breadcrumb category from the product page itself.

The output is saved as CSV, JSON, and Markdown files.
The 'description' field in the output is repurposed to store the category path
(breadcrumb) rather than the long product description.
"""

import argparse
import csv
import json
import os
import sys
import time
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

# ========== Configuration ==========
BASE_DOMAIN = "https://aldawaaegy.com"
DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ar,en;q=0.8",
}
REQUEST_DELAY = 0.6          # seconds between requests
PARSER = "html.parser"       # no external parser needed


# ========== Helper Functions ==========
def fetch(url, session, retries=3, timeout=20):
    """
    Perform an HTTP GET request with retry logic.
    Returns a Response object or None if all attempts fail.
    """
    for attempt in range(1, retries + 1):
        try:
            resp = session.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
            resp.raise_for_status()
            return resp
        except requests.RequestException:
            time.sleep(1.0 * attempt)
    print(f"[WARNING] Failed to load {url} after {retries} attempts.", file=sys.stderr)
    return None


def normalize_collection_url(raw_input):
    """
    Convert a collection handle or full URL into a clean collection URL.
    """
    if raw_input.startswith("http"):
        parsed = urlparse(raw_input)
        path = parsed.path.rstrip("/")
        return f"{BASE_DOMAIN}{path}"
    handle = raw_input.strip("/")
    return f"{BASE_DOMAIN}/ar/collections/{handle}"


def collect_product_urls(collection_url, session, max_pages=0):
    """
    Iterate over collection pages and collect unique product URLs.
    Returns a list of (product_handle, full_product_url) tuples.
    """
    product_urls = []
    seen = set()
    page = 1

    while True:
        page_url = f"{collection_url}?page={page}"
        print(f"[INFO] Fetching collection page: {page_url}")
        resp = fetch(page_url, session)
        if resp is None:
            break

        soup = BeautifulSoup(resp.text, PARSER)
        links = soup.select('a[href*="/products/"]')
        new_handles = set()
        for a in links:
            href = a.get("href", "")
            if "/products/" not in href:
                continue
            full = urljoin(BASE_DOMAIN, href.split("?")[0])
            handle = full.rstrip("/").split("/products/")[-1]
            if handle not in seen:
                seen.add(handle)
                new_handles.add(handle)
                product_urls.append((handle, full))

        print(f"    -> New products found on this page: {len(new_handles)}")
        if not new_handles:
            break
        if max_pages and page >= max_pages:
            break
        page += 1
        time.sleep(REQUEST_DELAY)

    return product_urls


def get_product_json(handle, session):
    """
    Fetch product data from Shopify's /products/<handle>.js endpoint.
    Returns a parsed JSON dict or None.
    """
    url = f"{BASE_DOMAIN}/products/{handle}.js"
    resp = fetch(url, session)
    if resp is None:
        return None
    try:
        return resp.json()
    except json.JSONDecodeError:
        return None


def extract_breadcrumb_category(product_page_url, session):
    """
    Extract the breadcrumb category from the product page.
    Returns a string like 'Home > Men Care > ...' or empty string.
    """
    resp = fetch(product_page_url, session)
    if resp is None:
        return ""
    soup = BeautifulSoup(resp.text, PARSER)

    # Attempt 1: Common breadcrumb HTML elements
    selectors = (
        ".breadcrumb, .breadcrumbs, nav.breadcrumb, "
        "[class*='breadcrumb'] a, [class*='breadcrumb'] span"
    )
    candidates = soup.select(selectors)
    parts = []
    for el in candidates:
        txt = el.get_text(strip=True)
        if txt and txt not in parts:
            parts.append(txt)
    if parts:
        return " > ".join(parts)

    # Attempt 2: JSON-LD BreadcrumbList
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script.string or "{}")
        except (json.JSONDecodeError, TypeError):
            continue
        items = data.get("itemListElement") if isinstance(data, dict) else None
        if items:
            names = [it.get("name", "") for it in items if isinstance(it, dict)]
            names = [n for n in names if n]
            if names:
                return " > ".join(names)
    return ""


def build_product_record(handle, product_url, session, fetch_extra=True):
    """
    Build a product record dict using the Shopify JSON and optional extra data.
    The 'description' field is repurposed to hold the category breadcrumb.
    """
    data = get_product_json(handle, session)
    if data is None:
        return None

    product_id = data.get("id")
    name = data.get("title", "").strip()
    vendor = data.get("vendor", "").strip()

    variants = data.get("variants", [])
    first_variant = variants[0] if variants else {}

    price_cents = first_variant.get("price")
    price = round(price_cents / 100, 2) if isinstance(price_cents, (int, float)) else None

    currency = "EGP"
    available = data.get("available", False)
    availability = "in stock" if available else "sold out"

    images = data.get("images", []) or []
    images = [urljoin("https:", img) if img.startswith("//") else img for img in images]
    thumbnail_image = images[0] if images else ""
    gallery_images = ";".join(images)

    category_text = ""
    if fetch_extra:
        time.sleep(REQUEST_DELAY)
        category_text = extract_breadcrumb_category(product_url, session)

    return {
        "product_id": product_id,
        "name": name,
        "price": price,
        "currency": currency,
        "brand": vendor,
        "description": category_text,       
        "availability": availability,
        "url": product_url,
        "thumbnail_image": thumbnail_image,
        "gallery_images": gallery_images,
    }


# ========== Output Functions ==========
def save_csv(records, path):
    """Save records to a CSV file."""
    fieldnames = [
        "product_id", "name", "price", "currency", "brand",
        "description", "availability", "url",
        "thumbnail_image", "gallery_images"
    ]
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in records:
            writer.writerow(r)


def save_json(records, path):
    """Save records as a JSON file."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


def save_markdown(records, path, collection_url):
    """Generate a Markdown report."""
    lines = [
        f"# Products from: {collection_url}",
        "",
        f"**Total products:** {len(records)}",
        ""
    ]
    for r in records:
        lines.append(f"## {r['name']}")
        lines.append("")
        if r["thumbnail_image"]:
            lines.append(f"![{r['name']}]({r['thumbnail_image']})")
            lines.append("")
        lines.append(f"- **Product ID:** {r['product_id']}")
        lines.append(f"- **Price:** {r['price']} {r['currency']}")
        lines.append(f"- **Brand:** {r['brand'] or '-'}")
        lines.append(f"- **Category (description):** {r['description'] or '-'}")
        lines.append(f"- **Availability:** {r['availability']}")
        lines.append(f"- **URL:** {r['url']}")
        if r["gallery_images"]:
            imgs = r["gallery_images"].split(";")
            lines.append(f"- **Gallery images:** {len(imgs)}")
        lines.append("")
        lines.append("---")
        lines.append("")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# ========== Main Entry Point ==========
def main():
    parser = argparse.ArgumentParser(description="Scraper for aldawaaegy.com (modified fields)")
    parser.add_argument(
        "--collection", default="men-care-1",
        help="Collection handle (default: men-care-1)"
    )
    parser.add_argument(
        "--url", default=None,
        help="Full collection URL (overrides --collection)"
    )
    parser.add_argument(
        "--max-pages", type=int, default=0,
        help="Maximum pages to scrape (0 = unlimited)"
    )
    parser.add_argument(
        "--no-extra", action="store_true",
        help="Skip fetching category from product page (faster)"
    )
    parser.add_argument(
        "--limit", type=int, default=0,
        help="Limit number of products to scrape (0 = all)"
    )
    parser.add_argument(
        "--out-prefix", default="./aldawaa_products",
        help="Output file prefix (without extension)"
    )

    args = parser.parse_args()

    # Ensure output directory exists
    out_dir = os.path.dirname(args.out_prefix)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    collection_url = normalize_collection_url(args.url or args.collection)
    print(f"[INFO] Collection URL: {collection_url}")

    session = requests.Session()

    product_pairs = collect_product_urls(collection_url, session, max_pages=args.max_pages)
    print(f"[INFO] Total product URLs found: {len(product_pairs)}")

    if args.limit:
        product_pairs = product_pairs[:args.limit]
        print(f"[INFO] Limiting to first {len(product_pairs)} products")

    records = []
    for i, (handle, full_url) in enumerate(product_pairs, start=1):
        print(f"[{i}/{len(product_pairs)}] Processing: {handle}")
        rec = build_product_record(
            handle, full_url, session, fetch_extra=not args.no_extra
        )
        if rec:
            records.append(rec)
        time.sleep(REQUEST_DELAY)

    print(f"[INFO] Successfully scraped {len(records)} products")

    csv_path = f"{args.out_prefix}.csv"
    json_path = f"{args.out_prefix}.json"
    md_path = f"{args.out_prefix}.md"

    save_csv(records, csv_path)
    save_json(records, json_path)
    save_markdown(records, md_path, collection_url)

    print(f"[INFO] Files saved:\n  - {csv_path}\n  - {json_path}\n  - {md_path}")


if __name__ == "__main__":
    main()

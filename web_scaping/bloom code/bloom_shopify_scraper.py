#!/usr/bin/env python3
"""
Bloom Pharmacy - Shopify API Scraper v3 (Bilingual) - Robust & Optimized
========================================================================
- Product names: English (from Shopify API)
- Descriptions: English + Arabic (scraped from /ar/ product pages)
- Arabic category names extracted from embedded JS on Arabic product pages
- Robust 429 rate limit backoff and thread-safe connection pooling.

Author: Antigravity AI
Date: 2026-06-25
"""

import csv
import json
import time
import logging
import re
import sys
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from bs4 import BeautifulSoup

# ─────────────────────────────────────────────
#  Configuration
# ─────────────────────────────────────────────
BASE_URL          = "https://www.bloompharmacy.com"
OUTPUT_DIR        = Path("bloom_pharmacy_data")
LOG_FILE          = "scraper_v3_bilingual.log"

PRODUCTS_PER_PAGE = 250
REQUEST_DELAY     = 0.2        # delay between paginated API calls (seconds)
AR_PAGE_DELAY     = 0.05       # tiny delay between Arabic page fetches (seconds)
REQUEST_TIMEOUT   = 25
MAX_RETRIES       = 5          # More retries to survive temporary rate limits
AR_WORKERS        = 8          # Moderate parallel workers for Arabic page fetching
COLLECTION_WORKERS = 4          # Safe parallel workers for collection scraping

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ar,en-US;q=0.8,en;q=0.6",
    "Connection": "keep-alive",
}

# ─────────────────────────────────────────────
#  Logging (Windows-safe)
# ─────────────────────────────────────────────
class AsciiSafeStreamHandler(logging.StreamHandler):
    def emit(self, record):
        try:
            msg = self.format(record)
            msg = (msg.replace("\u2713", "[OK]").replace("\u2717", "[X]")
                      .replace("\u2192", "->").replace("\u2714", "[OK]"))
            self.stream.write(msg + self.terminator)
            self.flush()
        except Exception:
            self.handleError(record)

logging.basicConfig(level=logging.INFO, handlers=[])
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
_fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
_ch = AsciiSafeStreamHandler(sys.stdout); _ch.setFormatter(_fmt); logger.addHandler(_ch)
_fh = logging.FileHandler(LOG_FILE, encoding="utf-8"); _fh.setFormatter(_fmt); logger.addHandler(_fh)


# ─────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────
def clean_html(html: str) -> str:
    if not html:
        return ""
    text = re.sub(r"<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", text).strip()


def format_price(price_str) -> str:
    try:
        return str(round(float(price_str), 2))
    except (ValueError, TypeError):
        return str(price_str) if price_str else "0"


def safe_filename(name: str) -> str:
    name = re.sub(r"[^\w\s-]", "", name)
    name = name.strip().replace(" ", "_").lower()
    return re.sub(r"_+", "_", name)


def safe_get_json(session: requests.Session, url: str) -> Optional[dict]:
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = session.get(url, timeout=REQUEST_TIMEOUT)
            if resp.status_code == 200:
                return resp.json()
            if resp.status_code in (404, 410):
                return None
            if resp.status_code == 429:
                backoff = 5.0 * attempt
                logger.warning(f"HTTP 429 Rate Limited. Sleeping {backoff}s before retry (attempt {attempt}): {url}")
                time.sleep(backoff)
                continue
            logger.warning(f"HTTP {resp.status_code} (attempt {attempt}): {url}")
        except requests.RequestException as exc:
            logger.warning(f"Request error (attempt {attempt}): {exc}")
        if attempt < MAX_RETRIES:
            time.sleep(REQUEST_DELAY * attempt)
    return None


def safe_get_html(session: requests.Session, url: str) -> Optional[str]:
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = session.get(url, timeout=REQUEST_TIMEOUT)
            if resp.status_code == 200:
                return resp.text
            if resp.status_code in (404, 410):
                return None
            if resp.status_code == 429:
                backoff = 6.0 * attempt
                logger.warning(f"HTML HTTP 429 Rate Limited. Sleeping {backoff}s before retry (attempt {attempt}): {url}")
                time.sleep(backoff)
                continue
        except requests.RequestException as exc:
            logger.warning(f"HTML fetch error (attempt {attempt}): {exc}")
        if attempt < MAX_RETRIES:
            time.sleep(AR_PAGE_DELAY * attempt)
    return None


# ─────────────────────────────────────────────
#  Arabic content extractor
# ─────────────────────────────────────────────
def extract_arabic_content(html: str) -> dict:
    """
    Parse an Arabic product page and extract:
    - Arabic product description (body text)
    - Arabic category names (from Klaviyo JS Categories array)
    """
    result = {"description_ar": "", "categories_ar": []}
    if not html:
        return result

    soup = BeautifulSoup(html, "html.parser")

    # 1. Arabic description: look for <div class="product__description"> or
    #    any div with Arabic text in the product body area
    desc_ar = ""
    for selector in [
        ".product__description",
        ".product-description",
        "[class*='product'][class*='desc']",
        ".rte",
    ]:
        elem = soup.select_one(selector)
        if elem:
            text = elem.get_text(separator=" ", strip=True)
            # Check if it contains Arabic characters
            if re.search(r'[\u0600-\u06FF]', text):
                desc_ar = text
                break

    # 2. Fallback: look at all script tags for Klaviyo Categories array
    categories_ar = []
    for script in soup.find_all("script"):
        text = script.string or ""
        # Look for: Categories: ["...arabic...", ...]
        match = re.search(r'Categories\s*:\s*(\[.*?\])', text, re.DOTALL)
        if match:
            try:
                cats_raw = json.loads(match.group(1))
                for cat in cats_raw:
                    if isinstance(cat, str) and re.search(r'[\u0600-\u06FF]', cat):
                        categories_ar.append(cat)
            except json.JSONDecodeError:
                pass
            break

    # 3. Try to get Arabic description from JSON-LD (sometimes stores add Arabic there)
    for script in soup.find_all("script", {"type": "application/ld+json"}):
        try:
            data = json.loads(script.string or "")
            if isinstance(data, dict) and data.get("@type") == "Product":
                desc_candidate = data.get("description", "")
                if re.search(r'[\u0600-\u06FF]', desc_candidate):
                    desc_ar = desc_candidate
                    break
        except (json.JSONDecodeError, AttributeError):
            pass

    result["description_ar"] = desc_ar
    result["categories_ar"]  = categories_ar
    return result


# ─────────────────────────────────────────────
#  Product parser (English fields from API)
# ─────────────────────────────────────────────
CSV_FIELDS = [
    # Identity
    "product_id", "handle",
    # English fields
    "name_en", "vendor", "product_type", "category_en",
    "tags", "sku",
    # Pricing
    "price", "compare_at_price", "discount_pct", "currency",
    # Stock
    "availability", "variant_count",
    # Arabic fields
    "name_ar", "description_en", "description_ar", "categories_ar",
    # Media
    "url", "thumbnail_image", "gallery_images",
    # Timestamps
    "published_at", "created_at", "updated_at",
    # Variants
    "option_names", "option_values",
]


def parse_product(raw: dict, collection_name: str = "") -> dict:
    """Parse a Shopify product dict into our bilingual schema."""
    product_id   = raw.get("id", "")
    handle       = raw.get("handle", "")
    title        = (raw.get("title") or "").strip()
    vendor       = (raw.get("vendor") or "").strip()
    product_type = (raw.get("product_type") or "").strip()
    tags         = raw.get("tags") or []
    body_html    = raw.get("body_html") or ""
    desc_en      = clean_html(body_html)
    published    = raw.get("published_at", "")
    created      = raw.get("created_at", "")
    updated      = raw.get("updated_at", "")
    url          = f"{BASE_URL}/products/{handle}" if handle else ""

    # Variants
    variants = raw.get("variants") or []
    prices, compare_prices, skus, available_flags = [], [], [], []
    for v in variants:
        p = v.get("price"); c = v.get("compare_at_price")
        if p is not None: prices.append(format_price(p))
        if c: compare_prices.append(format_price(c))
        sku = (v.get("sku") or "").strip()
        if sku: skus.append(sku)
        available_flags.append(bool(v.get("available")))

    price            = prices[0] if prices else "0"
    compare_at_price = compare_prices[0] if compare_prices else ""
    sku              = skus[0] if skus else ""
    availability     = "in stock" if any(available_flags) else "out of stock"
    variant_count    = len(variants)

    discount_pct = ""
    if price and compare_at_price:
        try:
            orig = float(compare_at_price); curr = float(price)
            if orig > curr > 0:
                discount_pct = f"{round((orig - curr) / orig * 100, 1)}%"
        except (ValueError, ZeroDivisionError):
            pass

    # Images
    images     = raw.get("images") or []
    image_urls = [img.get("src", "") for img in images if img.get("src")]
    thumbnail  = image_urls[0] if image_urls else ""
    gallery    = "|".join(image_urls)

    # Options (skip "Title" default)
    options      = raw.get("options") or []
    option_names  = [o.get("name", "") for o in options if o.get("name") != "Title"]
    option_values = ["|".join(o.get("values", [])) for o in options if o.get("name") != "Title"]

    category_en = collection_name or product_type or (tags[0] if tags else "")

    return {
        "product_id":       str(product_id),
        "handle":           handle,
        "name_en":          title,
        "name_ar":          "",           # filled in by Arabic page fetch
        "vendor":           vendor,
        "product_type":     product_type,
        "category_en":      category_en,
        "tags":             ", ".join(tags),
        "sku":              sku,
        "price":            price,
        "compare_at_price": compare_at_price,
        "discount_pct":     discount_pct,
        "currency":         "EGP",
        "availability":     availability,
        "variant_count":    variant_count,
        "url":              url,
        "thumbnail_image":  thumbnail,
        "gallery_images":   gallery,
        "description_en":   desc_en,
        "description_ar":   "",           # filled in by Arabic page fetch
        "categories_ar":    "",           # filled in by Arabic page fetch
        "published_at":     published,
        "created_at":       created,
        "updated_at":       updated,
        "option_names":     " | ".join(option_names),
        "option_values":    " ; ".join(option_values),
    }


# ─────────────────────────────────────────────
#  Arabic content fetcher (Worker)
# ─────────────────────────────────────────────
def fetch_arabic_for_product(product: dict, session: requests.Session) -> dict:
    """
    Given a product dict, fetch its Arabic page and enrich it in-place.
    Returns the enriched product dict.
    """
    handle = product.get("handle", "")
    if not handle:
        return product

    ar_url = f"{BASE_URL}/ar/products/{handle}"
    html   = safe_get_html(session, ar_url)
    if html:
        ar_data = extract_arabic_content(html)
        product["description_ar"] = ar_data["description_ar"]
        product["categories_ar"]  = " | ".join(ar_data["categories_ar"])
        # Arabic product name: check if og:title contains Arabic
        soup = BeautifulSoup(html, "html.parser")
        og_title = soup.find("meta", {"property": "og:title"})
        if og_title:
            ar_title = og_title.get("content", "")
            if re.search(r'[\u0600-\u06FF]', ar_title):
                product["name_ar"] = ar_title

    time.sleep(AR_PAGE_DELAY)
    return product


# ─────────────────────────────────────────────
#  Scraper
# ─────────────────────────────────────────────
class BloomBilingualScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        
        # Optimize connection pool size for high concurrency
        adapter = requests.adapters.HTTPAdapter(pool_connections=50, pool_maxsize=50)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
        
        self.all_products: List[dict] = []
        self.collections:  List[dict] = []

    # ── Shopify JSON API helpers ─────────────────
    def _fetch_paginated(self, base_url: str, key: str,
                         parser=None, label="") -> list:
        results = []
        for page in range(1, 100):
            url  = f"{base_url}?limit={PRODUCTS_PER_PAGE}&page={page}"
            data = safe_get_json(self.session, url)
            if not data:
                break
            batch = data.get(key, [])
            if not batch:
                break
            results.extend(batch if parser is None
                           else [parser(r) for r in batch])
            if label:
                logger.info(f"  {label} page {page}: +{len(batch)} (total: {len(results)})")
            if len(batch) < PRODUCTS_PER_PAGE:
                break
            time.sleep(REQUEST_DELAY)
        return results

    def fetch_global_products(self) -> List[dict]:
        logger.info("\nFetching products via /products.json (up to 5,000)...")
        raw = []
        for page in range(1, 21):
            url  = f"{BASE_URL}/products.json?limit={PRODUCTS_PER_PAGE}&page={page}"
            data = safe_get_json(self.session, url)
            if not data: break
            batch = data.get("products", [])
            if not batch: break
            raw.extend(batch)
            logger.info(f"  Page {page}: +{len(batch)} (total: {len(raw)})")
            if len(batch) < PRODUCTS_PER_PAGE: break
            time.sleep(REQUEST_DELAY)
        parsed = [parse_product(r) for r in raw]
        logger.info(f"[OK] Global fetch: {len(parsed)} products")
        return parsed

    def fetch_all_collections(self) -> List[dict]:
        logger.info("Fetching all collections index...")
        cols = self._fetch_paginated(f"{BASE_URL}/collections.json",
                                     "collections", label="Collections")
        logger.info(f"[OK] Collections found: {len(cols)}")
        self.collections = cols
        return cols

    def fetch_collection_products(self, handle: str, name: str) -> List[dict]:
        raw = self._fetch_paginated(
            f"{BASE_URL}/collections/{handle}/products.json",
            "products")
        return [parse_product(r, collection_name=name) for r in raw]

    def fetch_collection_worker(self, handle: str, name: str) -> tuple:
        try:
            prods = self.fetch_collection_products(handle, name)
            return handle, name, prods
        except Exception as e:
            logger.error(f"Error fetching collection {name} ({handle}): {e}")
            return handle, name, []

    @staticmethod
    def dedupe(products: List[dict]) -> List[dict]:
        seen, unique = set(), []
        for p in products:
            pid = p.get("product_id", p.get("url"))
            if pid not in seen:
                seen.add(pid)
                unique.append(p)
        return unique

    # ── Arabic enrichment ─────────────────────────
    def enrich_arabic(self, products: List[dict]) -> List[dict]:
        total   = len(products)
        logger.info(f"\nFetching Arabic content for {total:,} products "
                    f"({AR_WORKERS} parallel workers)...")

        enriched = [None] * total
        completed = 0

        with ThreadPoolExecutor(max_workers=AR_WORKERS) as executor:
            future_to_idx = {
                executor.submit(fetch_arabic_for_product, dict(p), self.session): i
                for i, p in enumerate(products)
            }
            for future in as_completed(future_to_idx):
                idx = future_to_idx[future]
                try:
                    enriched[idx] = future.result()
                except Exception as exc:
                    logger.warning(f"Arabic fetch error for product {idx}: {exc}")
                    enriched[idx] = products[idx]
                completed += 1
                if completed % 100 == 0 or completed == total:
                    logger.info(f"  Arabic progress: {completed:,}/{total:,} "
                                f"({completed/total*100:.1f}%)")

        return enriched

    # ── Save helpers ──────────────────────────────
    def _write_csv(self, path: Path, products: List[dict]):
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDS, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(products)

    def _write_json(self, path: Path, data):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def save_collection_files(self, name: str, products: List[dict]):
        safe = safe_filename(name)
        csv_path  = OUTPUT_DIR / f"bloom_{safe}.csv"
        json_path = OUTPUT_DIR / f"bloom_{safe}.json"
        try:
            self._write_csv(csv_path, products)
            logger.info(f"      [OK] CSV  -> {csv_path.name} ({len(products):,} rows)")
        except Exception as e:
            logger.error(f"      CSV error: {e}")
        try:
            self._write_json(json_path, products)
            logger.info(f"      [OK] JSON -> {json_path.name}")
        except Exception as e:
            logger.error(f"      JSON error: {e}")

    def save_all_products(self):
        csv_path  = OUTPUT_DIR / "bloom_ALL_products.csv"
        json_path = OUTPUT_DIR / "bloom_ALL_products.json"
        try:
            self._write_csv(csv_path, self.all_products)
            mb = csv_path.stat().st_size / 1_048_576
            logger.info(f"[OK] ALL CSV : {csv_path.name} "
                        f"({len(self.all_products):,} rows, {mb:.1f} MB)")
        except Exception as e:
            logger.error(f"ALL CSV error: {e}")
        try:
            self._write_json(json_path, self.all_products)
            mb = json_path.stat().st_size / 1_048_576
            logger.info(f"[OK] ALL JSON: {json_path.name} "
                        f"({len(self.all_products):,} items, {mb:.1f} MB)")
        except Exception as e:
            logger.error(f"ALL JSON error: {e}")

    def save_collections_index(self, collections: List[dict]):
        csv_path  = OUTPUT_DIR / "bloom_collections_index.csv"
        json_path = OUTPUT_DIR / "bloom_collections_index.json"
        rows = []
        for c in collections:
            img = c.get("image") or {}
            rows.append({
                "id":             c.get("id", ""),
                "title":          c.get("title", ""),
                "handle":         c.get("handle", ""),
                "description":    clean_html(c.get("description") or ""),
                "products_count": c.get("products_count", 0),
                "published_at":   c.get("published_at", ""),
                "updated_at":     c.get("updated_at", ""),
                "image_src":      img.get("src", ""),
            })
        try:
            with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
                writer.writeheader()
                writer.writerows(rows)
            logger.info(f"[OK] Collections CSV: {csv_path.name} ({len(rows):,})")
        except Exception as e:
            logger.error(f"Collections CSV error: {e}")
        try:
            self._write_json(json_path, collections)
            logger.info(f"[OK] Collections JSON: {json_path.name}")
        except Exception as e:
            logger.error(f"Collections JSON error: {e}")

    # ── Main ──────────────────────────────────────
    def scrape_all(self):
        logger.info("=" * 70)
        logger.info("BLOOM PHARMACY - BILINGUAL SCRAPER v3 (OPTIMIZED & ROBUST)")
        logger.info(f"Target : {BASE_URL}")
        logger.info(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 70)
        OUTPUT_DIR.mkdir(exist_ok=True)

        # ── Phase 1: English product data ──────────
        global_products = self.fetch_global_products()
        collections     = self.fetch_all_collections()
        self.save_collections_index(collections)

        MAIN_COLLECTIONS = [
            ("pharmacy-prescriptions",   "Pharmacy Prescriptions"),
            ("shophealth-wellness",       "Health & Wellness"),
            ("shopbeauty-cosmetics",      "Beauty & Cosmetics"),
            ("shopdermocosmetics",        "Dermocosmetics"),
            ("shopmother-baby-care",      "Mother & Baby Care"),
            ("shopk-beauty",             "K-Beauty"),
            ("shopthe-local-shelf",       "The Local Shelf"),
            ("on-sale",                   "On Sale"),
            ("fitness-nutrition",         "Fitness & Nutrition"),
            ("vitamins-supplements",      "Vitamins & Supplements"),
            ("hair-care",                 "Hair Care"),
            ("skin-care",                 "Skin Care"),
            ("oral-care",                 "Oral Care"),
            ("perfumes-fragrances",       "Perfumes & Fragrances"),
            ("home-scents-spaces",        "Home Scents & Spaces"),
            ("foot-nail-care",            "Foot & Nail Care"),
            ("eye-care",                  "Eye Care"),
            ("bath-body-care",            "Bath & Body Care"),
            ("feminine-care",             "Feminine Care"),
            ("allergy-asthma",            "Allergy & Asthma"),
            ("acne-blemishes-blackheads", "Acne Blemishes & Blackheads"),
            ("sun-care",                  "Sun Care"),
            ("anti-aging",                "Anti-Aging"),
            ("face-moisturizers",         "Face Moisturizers"),
            ("hair-color",                "Hair Color"),
            ("baby-food-formula",         "Baby Food & Formula"),
            ("nursing-feeding",           "Nursing & Feeding"),
            ("diapers-wipes",             "Diapers & Wipes"),
        ]

        logger.info(f"\nScraping {len(MAIN_COLLECTIONS)} main categories in parallel (concurrency: {COLLECTION_WORKERS})...")
        all_collected   = list(global_products)
        main_cat_prods: Dict[str, List[dict]] = {}

        with ThreadPoolExecutor(max_workers=COLLECTION_WORKERS) as executor:
            futures = {
                executor.submit(self.fetch_collection_worker, slug, name): name
                for slug, name in MAIN_COLLECTIONS
            }
            completed = 0
            for future in as_completed(futures):
                name = futures[future]
                _, _, prods = future.result()
                if prods:
                    main_cat_prods[name] = prods
                    all_collected.extend(prods)
                    logger.info(f"  [{completed+1}/{len(MAIN_COLLECTIONS)}] {name} -> {len(prods):,} products")
                else:
                    logger.warning(f"  [{completed+1}/{len(MAIN_COLLECTIONS)}] {name} -> No products")
                completed += 1

        # Scrape remaining collections in parallel
        logger.info(f"\nScraping remaining collections in parallel (concurrency: {COLLECTION_WORKERS})...")
        main_slugs = {s for s, _ in MAIN_COLLECTIONS}
        remaining  = [c for c in collections
                      if c["handle"] not in main_slugs
                      and c.get("products_count", 0) > 0]
        logger.info(f"  {len(remaining):,} additional collections to scrape")

        with ThreadPoolExecutor(max_workers=COLLECTION_WORKERS) as executor:
            futures = {
                executor.submit(self.fetch_collection_worker, c["handle"], c["title"]): c
                for c in remaining
            }
            completed = 0
            for future in as_completed(futures):
                c = futures[future]
                _, _, prods = future.result()
                if prods:
                    all_collected.extend(prods)
                completed += 1
                if completed % 50 == 0 or completed == len(remaining):
                    logger.info(f"  Collection progress: {completed}/{len(remaining)}")

        # Deduplicate
        logger.info("\nDeduplicating...")
        unique = self.dedupe(all_collected)
        logger.info(f"  Total collected: {len(all_collected):,}")
        logger.info(f"  Unique products: {len(unique):,}")

        # ── Phase 2: Arabic enrichment ─────────────
        logger.info("\n" + "=" * 70)
        logger.info(f"PHASE 2: FETCHING ARABIC CONTENT (CONCURRENT: {AR_WORKERS})")
        logger.info("=" * 70)
        unique = self.enrich_arabic(unique)
        self.all_products = [p for p in unique if p is not None]

        # ── Phase 3: Save enriched category files ──
        logger.info("\nSaving enriched category files...")
        url_to_product = {p["url"]: p for p in self.all_products}

        for name, prods in main_cat_prods.items():
            enriched_prods = [url_to_product.get(p["url"], p) for p in prods]
            self.save_collection_files(name, enriched_prods)

        # ── Phase 4: Save combined output ──────────
        logger.info("\n" + "=" * 70)
        logger.info("SAVING COMBINED OUTPUT")
        logger.info("=" * 70)
        self.save_all_products()
        self.print_summary(main_cat_prods)

    def print_summary(self, main_map: dict):
        ar_with_desc = sum(1 for p in self.all_products if p.get("description_ar"))
        ar_with_cats = sum(1 for p in self.all_products if p.get("categories_ar"))
        logger.info("\n" + "=" * 70)
        logger.info("SCRAPING COMPLETE - SUMMARY")
        logger.info("=" * 70)
        logger.info(f"Total unique products     : {len(self.all_products):,}")
        logger.info(f"With Arabic description   : {ar_with_desc:,}")
        logger.info(f"With Arabic categories    : {ar_with_cats:,}")
        logger.info(f"Collections indexed       : {len(self.collections):,}")
        logger.info("\nMain categories:")
        for name, prods in sorted(main_map.items()):
            logger.info(f"  {name:<45} {len(prods):>6,}")
        logger.info(f"\nOutput: {OUTPUT_DIR.resolve()}")
        for f in sorted(OUTPUT_DIR.glob("bloom_*.csv")):
            mb = f.stat().st_size / 1_048_576
            logger.info(f"  {f.name:<55} {mb:6.2f} MB")
        logger.info("=" * 70)
        logger.info(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


# ─────────────────────────────────────────────
#  Entry point
# ─────────────────────────────────────────────
def main():
    scraper = BloomBilingualScraper()
    try:
        scraper.scrape_all()
    except KeyboardInterrupt:
        logger.warning("\nInterrupted. Saving partial data...")
        if scraper.all_products:
            scraper.save_all_products()
    except Exception as exc:
        logger.exception(f"Fatal error: {exc}")
        raise


if __name__ == "__main__":
    main()

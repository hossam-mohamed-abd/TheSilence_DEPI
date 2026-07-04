#!/usr/bin/env python3
"""
Bloom Pharmacy Fast Scraper (No Selenium required)
Uses direct HTTP requests with intelligent parsing
"""

import csv
import json
import time
import logging
from urllib.parse import urljoin, urlparse
from pathlib import Path
from typing import List, Dict, Optional

import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BASE_URL = "https://www.bloompharmacy.com"
OUTPUT_DIR = Path("bloom_pharmacy_data")
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}


class BloomPharmacyFastScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.products = []
        self.categories = {}

    def get_categories(self) -> Dict[str, str]:
        """Fetch categories from sitemap or hardcoded list"""
        logger.info("Using predefined categories...")
        return {
            'Skincare': 'skin-care',
            'Hair Care': 'hair-care',
            'Body Care': 'body-care',
            'Beauty Cosmetics': 'beauty-cosmetics',
            'Deodorant': 'deodorant',
            'Health Wellness': 'health-wellness',
            'Mother Baby': 'mother-baby-care',
            'Fragrances': 'fragrances',
            'Oral Care': 'oral-care',
            'Makeup': 'makeup',
        }

    def scrape_category(self, category_name: str, category_slug: str, max_pages: Optional[int] = None) -> List[Dict]:
        """Scrape a category"""
        logger.info(f"\n=== Scraping: {category_name} ({category_slug}) ===")
        all_products = []
        page = 1

        while True:
            if max_pages and page > max_pages:
                break

            url = f"{BASE_URL}/collections/{category_slug}?page={page}"
            logger.info(f"Page {page}: {url}")

            try:
                response = self.session.get(url, timeout=15)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')

                products = self.extract_products(soup, category_name)
                if not products:
                    logger.info("No products found - stopping pagination")
                    break

                all_products.extend(products)
                logger.info(f"Extracted {len(products)} products")

                # Check for next page
                if not self.has_next_page(soup):
                    logger.info("Last page reached")
                    break

                page += 1
                time.sleep(2)

            except requests.RequestException as e:
                logger.error(f"Request error: {e}")
                break

        logger.info(f"Total from {category_name}: {len(all_products)} products\n")
        return all_products

    def extract_products(self, soup: BeautifulSoup, category: str) -> List[Dict]:
        """Extract products from page HTML"""
        products = []

        # Try multiple selectors
        selectors = [
            'div[class*="ProductCard"]',
            'li[data-product-handle]',
            'div[data-product-id]',
            'article[class*="product"]',
            'div.product-item',
        ]

        items = []
        for selector in selectors:
            items = soup.select(selector)
            if items:
                logger.debug(f"Found {len(items)} items with selector: {selector}")
                break

        for item in items[:50]:  # Limit per page
            try:
                product = self.parse_product(item, category)
                if product and product.get('name'):
                    products.append(product)
            except Exception as e:
                logger.debug(f"Parse error: {e}")

        return products

    def parse_product(self, item, category: str) -> Optional[Dict]:
        """Parse individual product"""
        try:
            # Name
            name = None
            for selector in ['h3', 'h2', 'a[data-product-title]', '[class*="title"]']:
                elem = item.select_one(selector)
                if elem:
                    name = elem.get_text(strip=True)
                    if name and len(name) > 5:  # Filter out short text
                        break

            # URL (unique identifier)
            url = None
            product_id = None
            for link in item.find_all('a', href=True):
                href = link['href']
                if '/products/' in href:
                    url = href if href.startswith('http') else urljoin(BASE_URL, href)
                    product_id = urlparse(url).path.split('/products/')[-1].split('?')[0]
                    break

            if not url or not product_id:
                return None

            # Price - extract just the number
            price = '0'
            for elem in item.find_all(['span', 'div', 'p']):
                text = elem.get_text(strip=True)
                # Look for currency
                if 'EGP' in text or '£' in text or '€' in text:
                    # Extract numbers
                    import re
                    numbers = re.findall(r'\d+\.?\d*', text)
                    if numbers:
                        # Take the first significant number (usually the sale price)
                        price = numbers[0]
                        break

            # Image
            image = ''
            img = item.find('img')
            if img:
                image = img.get('src') or img.get('data-src') or ''
                if image and not image.startswith('http'):
                    image = urljoin(BASE_URL, image)

            # Brand
            brand = self.extract_brand(name)

            if not name or len(name) < 5:
                return None

            return {
                'product_id': product_id,
                'name': name,
                'name_en': name,
                'price': price,
                'currency': 'EGP',
                'brand': brand,
                'category': category,
                'availability': 'in stock',
                'url': url,
                'thumbnail_image': image,
                'gallery_images': [image] if image else [],
                'description': '',
                'specifications': {'brand': brand} if brand else {}
            }

        except Exception as e:
            logger.debug(f"Error parsing: {e}")
            return None

    def extract_brand(self, name: str) -> str:
        """Extract brand from product name"""
        if not name:
            return ''
        # Common brands to extract
        brands = ['Nivea', 'The Ordinary', 'CeraVe', 'La Roche', 'Vichy', 'Revlon', 'MAC']
        for brand in brands:
            if brand.lower() in name.lower():
                return brand
        # Fallback: first word
        return name.split()[0] if name else ''

    def has_next_page(self, soup: BeautifulSoup) -> bool:
        """Check if pagination has next page"""
        next_link = soup.find('a', {'rel': 'next'}) or soup.find('a', class_=lambda x: x and 'next' in x.lower())
        return bool(next_link)

    def save_csv(self, filename: str = 'bloom_pharmacy_products.csv'):
        """Save to CSV"""
        if not self.products:
            logger.warning("No products to save")
            return

        OUTPUT_DIR.mkdir(exist_ok=True)
        filepath = OUTPUT_DIR / filename

        fieldnames = [
            'product_id', 'name', 'name_en', 'price', 'currency', 'brand',
            'category', 'availability', 'url', 'thumbnail_image',
            'gallery_images', 'description', 'specifications'
        ]

        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()

                for product in self.products:
                    row = {k: product.get(k, '') for k in fieldnames}
                    if isinstance(row['gallery_images'], list):
                        row['gallery_images'] = '|'.join(row['gallery_images'])
                    if isinstance(row['specifications'], dict):
                        row['specifications'] = json.dumps(row['specifications'])
                    writer.writerow(row)

            logger.info(f"✓ Saved {len(self.products)} products to {filepath}")

        except Exception as e:
            logger.error(f"CSV save error: {e}")

    def save_json(self, filename: str = 'bloom_pharmacy_products.json'):
        """Save to JSON"""
        if not self.products:
            return

        OUTPUT_DIR.mkdir(exist_ok=True)
        filepath = OUTPUT_DIR / filename

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.products, f, ensure_ascii=False, indent=2)

            logger.info(f"✓ Saved {len(self.products)} products to {filepath}")

        except Exception as e:
            logger.error(f"JSON save error: {e}")

    def scrape_all(self, max_pages_per_category: Optional[int] = None):
        """Scrape all categories"""
        self.categories = self.get_categories()

        for category_name, category_slug in self.categories.items():
            try:
                products = self.scrape_category(category_name, category_slug, max_pages_per_category)
                self.products.extend(products)
            except Exception as e:
                logger.error(f"Error scraping {category_name}: {e}")

        # Remove duplicates by URL
        seen_urls = set()
        unique_products = []
        for p in self.products:
            if p.get('url') not in seen_urls:
                seen_urls.add(p.get('url'))
                unique_products.append(p)

        self.products = unique_products
        logger.info(f"Deduplicated to {len(self.products)} unique products")


def main():
    """Main execution"""
    logger.info("=" * 50)
    logger.info("Bloom Pharmacy Fast Scraper")
    logger.info("=" * 50)

    scraper = BloomPharmacyFastScraper()

    # Scrape (adjust max_pages_per_category: None for all pages)
    scraper.scrape_all(max_pages_per_category=3)

    # Save
    scraper.save_csv()
    scraper.save_json()

    logger.info("=" * 50)
    logger.info(f"Total products: {len(scraper.products)}")
    logger.info("Done!")


if __name__ == "__main__":
    main()

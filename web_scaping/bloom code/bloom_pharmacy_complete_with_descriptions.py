#!/usr/bin/env python3
"""
Bloom Pharmacy Complete Web Scraper with Descriptions
Scrapes ALL categories, ALL products, and detailed descriptions in English
"""

import csv
import json
import time
import logging
from urllib.parse import urljoin, urlparse
from pathlib import Path
from typing import List, Dict, Optional
import re

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


class BloomPharmacyDescriptionScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.products = []
        self.categories = {}

    def discover_all_categories(self) -> Dict[str, str]:
        """Discover ALL categories from the website"""
        logger.info("Discovering all categories from website...")
        categories = {}

        try:
            response = self.session.get(f"{BASE_URL}/collections", timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            links = soup.find_all('a', href=lambda x: x and '/collections/' in x)

            for link in links:
                href = link.get('href', '')
                text = link.get_text(strip=True)

                if '/collections/' in href and text and len(text) > 2:
                    slug = href.split('/collections/')[-1].split('?')[0].rstrip('/')

                    if slug and slug != 'collections' and not 'liquid error' in text.lower():
                        categories[text] = slug

            logger.info(f"Found {len(categories)} categories")
            return categories

        except Exception as e:
            logger.error(f"Error discovering categories: {e}")
            return self.get_default_categories()

    def get_default_categories(self) -> Dict[str, str]:
        """Fallback categories"""
        return {
            'Skincare': 'skin-care',
            'Hair Care': 'hair-care',
            'Beauty Cosmetics': 'beauty-cosmetics',
            'Health Wellness': 'health-wellness',
            'Mother Baby': 'mother-baby-care',
            'Oral Care': 'oral-care',
        }

    def scrape_category_all_pages(self, category_name: str, category_slug: str) -> List[Dict]:
        """Scrape ALL pages from a category"""
        logger.info(f"\n{'='*60}")
        logger.info(f"Scraping: {category_name} ({category_slug})")
        logger.info(f"{'='*60}")

        category_products = []
        page = 1
        consecutive_empty = 0

        while True:
            url = f"{BASE_URL}/collections/{category_slug}?page={page}"
            logger.info(f"Page {page}: {url}")

            try:
                response = self.session.get(url, timeout=15)

                if response.status_code == 404:
                    logger.info("Category not found (404)")
                    break

                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')

                products = self.extract_products(soup, category_name)

                if not products:
                    consecutive_empty += 1
                    logger.info(f"No products found (attempt {consecutive_empty})")

                    if consecutive_empty >= 3:
                        logger.info("No more products in this category")
                        break
                else:
                    consecutive_empty = 0
                    category_products.extend(products)
                    logger.info(f"✓ Extracted {len(products)} products (Total: {len(category_products)})")

                page += 1
                time.sleep(2)

            except requests.RequestException as e:
                logger.error(f"Request error: {e}")
                break
            except Exception as e:
                logger.error(f"Error: {e}")
                break

        logger.info(f"Total from {category_name}: {len(category_products)} products")
        return category_products

    def extract_products(self, soup: BeautifulSoup, category: str) -> List[Dict]:
        """Extract products from page"""
        products = []

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

        for item in items[:100]:
            try:
                product = self.parse_product_item(item, category)
                if product and product.get('name'):
                    products.append(product)
            except Exception as e:
                logger.debug(f"Parse error: {e}")

        return products

    def parse_product_item(self, item, category: str) -> Optional[Dict]:
        """Parse individual product"""
        try:
            # Name
            name = None
            for selector in ['h3', 'h2', 'a[data-product-title]', '[class*="title"]']:
                elem = item.select_one(selector)
                if elem:
                    name = elem.get_text(strip=True)
                    if name and len(name) > 5:
                        break

            # URL
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

            # Price
            price = '0'
            for elem in item.find_all(['span', 'div', 'p']):
                text = elem.get_text(strip=True)
                if 'EGP' in text or '£' in text or '€' in text:
                    numbers = re.findall(r'\d+\.?\d*', text)
                    if numbers:
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

            # Fetch description from product page
            description = self.fetch_product_description(url)

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
                'description': description,
                'specifications': {'brand': brand} if brand else {}
            }

        except Exception as e:
            logger.debug(f"Error parsing: {e}")
            return None

    def fetch_product_description(self, product_url: str) -> str:
        """Fetch product description from product detail page"""
        try:
            response = self.session.get(product_url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            # Try multiple selectors for description
            description = ""

            # Look for product description sections
            selectors = [
                'div[class*="product-description"]',
                'div[class*="description"]',
                '[class*="product-info"]',
                'section[class*="description"]',
                '[data-section="product-description"]',
            ]

            for selector in selectors:
                desc_elem = soup.select_one(selector)
                if desc_elem:
                    # Get all text but remove script and style tags
                    for tag in desc_elem.find_all(['script', 'style']):
                        tag.decompose()

                    description = desc_elem.get_text(separator=' ', strip=True)

                    # Clean up whitespace
                    description = ' '.join(description.split())

                    if description and len(description) > 20:
                        break

            # If no description found in dedicated sections, try to get from meta
            if not description or len(description) < 20:
                # Try meta description
                meta_desc = soup.find('meta', {'name': 'description'})
                if meta_desc:
                    description = meta_desc.get('content', '')

            # Limit description to 500 characters
            if description:
                description = description[:500]

            return description

        except Exception as e:
            logger.debug(f"Error fetching description for {product_url}: {e}")
            return ""

    def extract_brand(self, name: str) -> str:
        """Extract brand from product name"""
        if not name:
            return ''

        common_brands = [
            'La Roche', 'The Ordinary', 'CeraVe', 'Vichy', 'Revlon', 'MAC',
            'Nivea', 'Dove', 'Maybelline', 'L\'Oreal', 'Neutrogena', 'Eucerin'
        ]

        for brand in common_brands:
            if brand.lower() in name.lower():
                return brand

        return name.split()[0] if name else ''

    def save_csv(self, filename: str = 'bloom_pharmacy_all_products.csv'):
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

    def save_json(self, filename: str = 'bloom_pharmacy_all_products.json'):
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

    def save_by_category_csv(self):
        """Save products grouped by category in separate CSV files"""
        OUTPUT_DIR.mkdir(exist_ok=True)

        categories_data = {}
        for product in self.products:
            cat = product.get('category', 'Uncategorized')
            if cat not in categories_data:
                categories_data[cat] = []
            categories_data[cat].append(product)

        fieldnames = [
            'product_id', 'name', 'name_en', 'price', 'currency', 'brand',
            'category', 'availability', 'url', 'thumbnail_image',
            'gallery_images', 'description', 'specifications'
        ]

        for category, products in categories_data.items():
            filename = f"bloom_pharmacy_{category.lower().replace(' ', '_').replace('&', 'and')}.csv"
            filepath = OUTPUT_DIR / filename

            try:
                with open(filepath, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()

                    for product in products:
                        row = {k: product.get(k, '') for k in fieldnames}
                        if isinstance(row['gallery_images'], list):
                            row['gallery_images'] = '|'.join(row['gallery_images'])
                        if isinstance(row['specifications'], dict):
                            row['specifications'] = json.dumps(row['specifications'])
                        writer.writerow(row)

                logger.info(f"✓ Saved {len(products)} {category} products to {filename}")
            except Exception as e:
                logger.error(f"Error saving {category} CSV: {e}")

    def save_by_category_json(self):
        """Save products grouped by category in separate JSON files"""
        OUTPUT_DIR.mkdir(exist_ok=True)

        categories_data = {}
        for product in self.products:
            cat = product.get('category', 'Uncategorized')
            if cat not in categories_data:
                categories_data[cat] = []
            categories_data[cat].append(product)

        for category, products in categories_data.items():
            filename = f"bloom_pharmacy_{category.lower().replace(' ', '_').replace('&', 'and')}.json"
            filepath = OUTPUT_DIR / filename

            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(products, f, ensure_ascii=False, indent=2)

                logger.info(f"✓ Saved {len(products)} {category} products to {filename}")
            except Exception as e:
                logger.error(f"Error saving {category} JSON: {e}")

    def scrape_all(self):
        """Scrape ALL categories with ALL pages and descriptions"""
        logger.info("\n" + "="*70)
        logger.info("BLOOM PHARMACY - COMPLETE SCRAPER WITH DESCRIPTIONS")
        logger.info("="*70)

        self.categories = self.discover_all_categories()

        if not self.categories:
            logger.error("No categories found!")
            return

        logger.info(f"\nFound {len(self.categories)} categories to scrape")

        for category_name, category_slug in self.categories.items():
            try:
                products = self.scrape_category_all_pages(category_name, category_slug)
                self.products.extend(products)
                time.sleep(1)
            except Exception as e:
                logger.error(f"Error scraping {category_name}: {e}")

        # Deduplicate by URL
        logger.info("\nDeduplicating products...")
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
    scraper = BloomPharmacyDescriptionScraper()

    try:
        # Scrape ALL categories and ALL pages with descriptions
        scraper.scrape_all()

        # Save combined files
        logger.info("\n" + "="*70)
        logger.info("SAVING FILES")
        logger.info("="*70)

        scraper.save_csv('bloom_pharmacy_all_products.csv')
        scraper.save_json('bloom_pharmacy_all_products.json')

        # Save by category
        logger.info("\nSaving products by category...")
        scraper.save_by_category_csv()
        scraper.save_by_category_json()

        # Final statistics
        logger.info("\n" + "="*70)
        logger.info("SCRAPING COMPLETE - SUMMARY")
        logger.info("="*70)
        logger.info(f"Total Products Scraped: {len(scraper.products)}")
        logger.info(f"Total Categories: {len(scraper.categories)}")

        # Category breakdown
        cat_counts = {}
        for p in scraper.products:
            cat = p.get('category', 'Uncategorized')
            cat_counts[cat] = cat_counts.get(cat, 0) + 1

        logger.info("\nProducts by Category:")
        for cat, count in sorted(cat_counts.items()):
            logger.info(f"  {cat}: {count}")

        # Check descriptions
        products_with_desc = sum(1 for p in scraper.products if p.get('description', '').strip())
        logger.info(f"\nProducts with descriptions: {products_with_desc}/{len(scraper.products)}")

        logger.info(f"\nOutput Location: {OUTPUT_DIR}/")
        logger.info("Files created:")
        logger.info("  - bloom_pharmacy_all_products.csv (combined)")
        logger.info("  - bloom_pharmacy_all_products.json (combined)")
        logger.info("  - bloom_pharmacy_[category].csv (by category)")
        logger.info("  - bloom_pharmacy_[category].json (by category)")
        logger.info("="*70)

    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise


if __name__ == "__main__":
    main()

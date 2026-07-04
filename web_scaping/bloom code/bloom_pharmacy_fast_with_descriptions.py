#!/usr/bin/env python3
"""
Fast Bloom Pharmacy Scraper - Gets all products quickly
Descriptions can be fetched in a second pass
"""

import csv
import json
import time
import logging
from urllib.parse import urljoin, urlparse
from pathlib import Path
from typing import List, Dict, Optional
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BASE_URL = "https://www.bloompharmacy.com"
OUTPUT_DIR = Path("bloom_pharmacy_data")
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}


class FastBloomPharmacyScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.products = []
        self.categories = {}

    def discover_all_categories(self) -> Dict[str, str]:
        """Discover ALL categories"""
        logger.info("Discovering categories...")
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
                    if slug and slug != 'collections' and 'liquid error' not in text.lower():
                        categories[text] = slug

            logger.info(f"Found {len(categories)} categories")
            return categories
        except Exception as e:
            logger.error(f"Error: {e}")
            return {}

    def scrape_category_all_pages(self, category_name: str, category_slug: str) -> List[Dict]:
        """Scrape all pages from category"""
        logger.info(f"Scraping: {category_name}")
        products = []
        page = 1
        consecutive_empty = 0

        while True:
            url = f"{BASE_URL}/collections/{category_slug}?page={page}"

            try:
                response = self.session.get(url, timeout=15)
                if response.status_code == 404:
                    break

                soup = BeautifulSoup(response.content, 'html.parser')
                page_products = self.extract_products(soup, category_name)

                if not page_products:
                    consecutive_empty += 1
                    if consecutive_empty >= 3:
                        break
                else:
                    consecutive_empty = 0
                    products.extend(page_products)
                    logger.info(f"  Page {page}: {len(page_products)} products (Total: {len(products)})")

                page += 1
                time.sleep(1)

            except Exception as e:
                logger.error(f"Error on page {page}: {e}")
                break

        logger.info(f"Total from {category_name}: {len(products)}")
        return products

    def extract_products(self, soup: BeautifulSoup, category: str) -> List[Dict]:
        """Extract products"""
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
                break

        for item in items[:100]:
            try:
                product = self.parse_product_item(item, category)
                if product and product.get('name'):
                    products.append(product)
            except:
                pass

        return products

    def parse_product_item(self, item, category: str) -> Optional[Dict]:
        """Parse product"""
        try:
            name = None
            for selector in ['h3', 'h2', 'a[data-product-title]']:
                elem = item.select_one(selector)
                if elem:
                    name = elem.get_text(strip=True)
                    if name and len(name) > 5:
                        break

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

            price = '0'
            for elem in item.find_all(['span', 'div', 'p']):
                text = elem.get_text(strip=True)
                if any(x in text for x in ['EGP', '£', '€']):
                    numbers = re.findall(r'\d+\.?\d*', text)
                    if numbers:
                        price = numbers[0]
                        break

            image = ''
            img = item.find('img')
            if img:
                image = img.get('src') or img.get('data-src') or ''
                if image and not image.startswith('http'):
                    image = urljoin(BASE_URL, image)

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
        except:
            return None

    def extract_brand(self, name: str) -> str:
        """Extract brand"""
        if not name:
            return ''
        brands = ['La Roche', 'The Ordinary', 'CeraVe', 'Vichy', 'Revlon', 'MAC']
        for brand in brands:
            if brand.lower() in name.lower():
                return brand
        return name.split()[0] if name else ''

    def fetch_description(self, product_url: str) -> str:
        """Fetch description from product page"""
        try:
            response = self.session.get(product_url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            # Remove scripts and styles
            for tag in soup.find_all(['script', 'style']):
                tag.decompose()

            # Look for description
            selectors = [
                'div[class*="product-description"]',
                'div[class*="description"]',
                '[class*="product-info"]',
            ]

            for selector in selectors:
                elem = soup.select_one(selector)
                if elem:
                    description = elem.get_text(separator=' ', strip=True)
                    description = ' '.join(description.split())
                    if description and len(description) > 20:
                        return description[:500]

            # Try meta description
            meta_desc = soup.find('meta', {'name': 'description'})
            if meta_desc:
                return meta_desc.get('content', '')[:500]

            return ''
        except:
            return ''

    def fetch_descriptions_for_products(self, max_workers: int = 3):
        """Fetch descriptions for all products using parallel requests"""
        logger.info(f"\nFetching descriptions for {len(self.products)} products...")
        logger.info(f"Using {max_workers} parallel workers...")

        updated_count = 0

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_product = {
                executor.submit(self.fetch_description, p['url']): i
                for i, p in enumerate(self.products)
            }

            completed = 0
            for future in as_completed(future_to_product):
                product_idx = future_to_product[future]
                try:
                    description = future.result()
                    if description:
                        self.products[product_idx]['description'] = description
                        updated_count += 1
                except Exception as e:
                    logger.debug(f"Error: {e}")

                completed += 1
                if completed % 50 == 0:
                    logger.info(f"Progress: {completed}/{len(self.products)} ({updated_count} with descriptions)")

        logger.info(f"Descriptions fetched: {updated_count}/{len(self.products)}")

    def save_csv(self, filename: str = 'bloom_pharmacy_all_products.csv'):
        """Save CSV"""
        if not self.products:
            return

        OUTPUT_DIR.mkdir(exist_ok=True)
        filepath = OUTPUT_DIR / filename

        fieldnames = [
            'product_id', 'name', 'name_en', 'price', 'currency', 'brand',
            'category', 'availability', 'url', 'thumbnail_image',
            'gallery_images', 'description', 'specifications'
        ]

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

        logger.info(f"✓ Saved to {filepath}")

    def save_json(self, filename: str = 'bloom_pharmacy_all_products.json'):
        """Save JSON"""
        if not self.products:
            return

        OUTPUT_DIR.mkdir(exist_ok=True)
        filepath = OUTPUT_DIR / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.products, f, ensure_ascii=False, indent=2)

        logger.info(f"✓ Saved to {filepath}")

    def save_by_category(self):
        """Save by category"""
        OUTPUT_DIR.mkdir(exist_ok=True)

        cat_products = {}
        for p in self.products:
            cat = p.get('category', 'Uncategorized')
            if cat not in cat_products:
                cat_products[cat] = []
            cat_products[cat].append(p)

        fieldnames = ['product_id', 'name', 'name_en', 'price', 'currency', 'brand',
                      'category', 'availability', 'url', 'thumbnail_image',
                      'gallery_images', 'description', 'specifications']

        for category, products in cat_products.items():
            filename = f"bloom_pharmacy_{category.lower().replace(' ', '_').replace('&', 'and')}"

            # CSV
            csv_path = OUTPUT_DIR / f"{filename}.csv"
            with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for p in products:
                    row = {k: p.get(k, '') for k in fieldnames}
                    if isinstance(row['gallery_images'], list):
                        row['gallery_images'] = '|'.join(row['gallery_images'])
                    if isinstance(row['specifications'], dict):
                        row['specifications'] = json.dumps(row['specifications'])
                    writer.writerow(row)

            # JSON
            json_path = OUTPUT_DIR / f"{filename}.json"
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(products, f, ensure_ascii=False, indent=2)

            logger.info(f"✓ {category}: {len(products)} products")

    def scrape_all(self, fetch_descriptions: bool = True):
        """Scrape all"""
        logger.info("\n" + "="*70)
        logger.info("BLOOM PHARMACY - FAST COMPLETE SCRAPER")
        logger.info("="*70)

        self.categories = self.discover_all_categories()

        if not self.categories:
            logger.error("No categories found!")
            return

        logger.info(f"\nCategories: {len(self.categories)}")

        for category_name, category_slug in self.categories.items():
            try:
                products = self.scrape_category_all_pages(category_name, category_slug)
                self.products.extend(products)
                time.sleep(0.5)
            except Exception as e:
                logger.error(f"Error: {e}")

        # Deduplicate
        logger.info("\nDeduplicating...")
        seen = set()
        unique = []
        for p in self.products:
            if p.get('url') not in seen:
                seen.add(p.get('url'))
                unique.append(p)

        self.products = unique
        logger.info(f"Unique products: {len(self.products)}")

        # Fetch descriptions if requested
        if fetch_descriptions:
            self.fetch_descriptions_for_products(max_workers=3)


def main():
    scraper = FastBloomPharmacyScraper()

    try:
        # Scrape with descriptions fetching
        scraper.scrape_all(fetch_descriptions=True)

        # Save files
        logger.info("\n" + "="*70)
        logger.info("SAVING FILES")
        logger.info("="*70)

        scraper.save_csv()
        scraper.save_json()

        logger.info("\nSaving by category...")
        scraper.save_by_category()

        # Summary
        logger.info("\n" + "="*70)
        logger.info("SUMMARY")
        logger.info("="*70)
        logger.info(f"Total Products: {len(scraper.products)}")

        with_desc = sum(1 for p in scraper.products if p.get('description', '').strip())
        logger.info(f"With Descriptions: {with_desc}/{len(scraper.products)}")

        logger.info(f"\nOutput: {OUTPUT_DIR}/")
        logger.info("="*70)

    except Exception as e:
        logger.error(f"Error: {e}")
        raise


if __name__ == "__main__":
    main()

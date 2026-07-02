#!/usr/bin/env python3
"""
Bloom Pharmacy Web Scraper
Scrapes products by category and saves to CSV and JSON formats
Uses Selenium for JavaScript-rendered content
"""

import csv
import json
import time
import logging
from urllib.parse import urljoin, urlparse
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    print("Selenium not installed. Install with: pip install selenium webdriver-manager")

from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BASE_URL = "https://www.bloompharmacy.com"
OUTPUT_DIR = Path("bloom_pharmacy_data")
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

class BloomPharmacyScraper:
    def __init__(self, use_selenium: bool = True):
        self.products = []
        self.categories = {}
        self.use_selenium = use_selenium and SELENIUM_AVAILABLE
        self.driver = None
        if self.use_selenium:
            self.setup_driver()

    def setup_driver(self):
        """Setup Selenium WebDriver"""
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            chrome_options = Options()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_argument(f'user-agent={HEADERS["User-Agent"]}')

            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=chrome_options
            )
            logger.info("Selenium WebDriver initialized")
        except Exception as e:
            logger.warning(f"Failed to setup Selenium: {e}")
            self.use_selenium = False

    def get_categories(self) -> Dict[str, str]:
        """Fetch all product categories"""
        logger.info("Fetching categories...")
        return self.get_default_categories()

    def get_default_categories(self) -> Dict[str, str]:
        """Return main categories"""
        return {
            'Skincare': 'skin-care',
            'Hair Care': 'hair-care',
            'Body Care': 'body-care',
            'Beauty & Cosmetics': 'beauty-cosmetics',
            'Health & Wellness': 'health-wellness',
            'Mother & Baby': 'mother-baby-care',
            'Fragrances': 'fragrances',
            'Oral Care': 'oral-care',
        }

    def scrape_category(self, category_name: str, category_slug: str, max_pages: Optional[int] = None) -> List[Dict]:
        """Scrape all products from a category"""
        logger.info(f"\n=== Scraping Category: {category_name} ({category_slug}) ===")
        category_products = []
        page = 1

        while True:
            if max_pages and page > max_pages:
                break

            url = f"{BASE_URL}/collections/{category_slug}?page={page}"
            logger.info(f"Scraping page {page}: {url}")

            try:
                products = self.scrape_page(url, category_name)
                if not products:
                    logger.info(f"No products found on page {page}")
                    break

                category_products.extend(products)
                logger.info(f"Extracted {len(products)} products from page {page}")
                page += 1
                time.sleep(2)

            except Exception as e:
                logger.error(f"Error scraping page {page}: {e}")
                break

        logger.info(f"Scraped {len(category_products)} products from {category_name}")
        return category_products

    def scrape_page(self, url: str, category: str) -> List[Dict]:
        """Scrape a single page"""
        products = []
        try:
            if self.use_selenium:
                self.driver.get(url)
                time.sleep(3)
                # Wait for products to load
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[class*='product']"))
                    )
                except:
                    pass
                html = self.driver.page_source
            else:
                import requests
                response = requests.get(url, headers=HEADERS, timeout=10)
                html = response.text

            soup = BeautifulSoup(html, 'html.parser')

            # Find product items - looking for common selectors
            selectors = [
                'div[class*="product-item"]',
                'div[class*="product-card"]',
                'article[class*="product"]',
                'div[data-product-id]',
                'li[data-product-id]',
            ]

            product_items = []
            for selector in selectors:
                product_items = soup.select(selector)
                if product_items:
                    logger.info(f"Found {len(product_items)} products using selector: {selector}")
                    break

            if not product_items:
                logger.warning("Could not find any product items on the page")
                return products

            for item in product_items:
                try:
                    product = self.parse_product_item(item, category)
                    if product:
                        products.append(product)
                except Exception as e:
                    logger.debug(f"Error parsing product item: {e}")

        except Exception as e:
            logger.error(f"Error scraping page {url}: {e}")

        return products

    def parse_product_item(self, item, category: str) -> Optional[Dict]:
        """Parse product item"""
        try:
            # Extract product information
            name = item.select_one('h3, h2, [class*="title"], [class*="name"]')
            name_text = name.get_text(strip=True) if name else None

            link = item.select_one('a[href*="/products/"]')
            url = link.get('href', '') if link else None
            if url and not url.startswith('http'):
                url = urljoin(BASE_URL, url)

            product_id = None
            if url:
                product_id = urlparse(url).path.split('/products/')[-1].rstrip('/')

            price = item.select_one('[class*="price"], .money')
            price_text = price.get_text(strip=True) if price else '0'
            price_text = price_text.replace('EGP', '').replace('£', '').strip()

            img = item.select_one('img')
            image = img.get('src') or img.get('data-src') if img else None
            if image and not image.startswith('http'):
                image = urljoin(BASE_URL, image)

            brand_elem = item.select_one('[class*="brand"], [class*="vendor"]')
            brand = brand_elem.get_text(strip=True) if brand_elem else self.extract_brand(name_text)

            if not name_text:
                return None

            return {
                'product_id': product_id or '',
                'name': name_text,
                'name_en': name_text,
                'price': price_text,
                'currency': 'EGP',
                'brand': brand or 'Unknown',
                'category': category,
                'availability': 'in stock',
                'url': url or '',
                'thumbnail_image': image or '',
                'gallery_images': [image] if image else [],
                'description': '',
                'specifications': {'brand': brand or 'Unknown'} if brand else {}
            }

        except Exception as e:
            logger.debug(f"Error parsing product: {e}")
            return None

    def extract_brand(self, name: str) -> str:
        """Extract brand from name"""
        if not name:
            return ''
        return name.split()[0] if name else ''

    def scrape_all(self, max_pages_per_category: Optional[int] = None):
        """Scrape all categories"""
        self.categories = self.get_categories()

        for category_name, category_slug in self.categories.items():
            products = self.scrape_category(category_name, category_slug, max_pages_per_category)
            self.products.extend(products)

    def close(self):
        """Close the driver"""
        if self.driver:
            self.driver.quit()

    def save_csv(self, filename: str = 'bloom_pharmacy_products.csv'):
        """Save products to CSV file"""
        if not self.products:
            logger.warning("No products to save")
            return

        self.output_dir.mkdir(exist_ok=True)
        filepath = self.output_dir / filename

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
                    row = {field: product.get(field, '') for field in fieldnames}
                    # Convert lists to strings
                    if isinstance(row['gallery_images'], list):
                        row['gallery_images'] = '|'.join(row['gallery_images'])
                    if isinstance(row['specifications'], dict):
                        row['specifications'] = json.dumps(row['specifications'])
                    writer.writerow(row)

            logger.info(f"Saved {len(self.products)} products to {filepath}")

        except Exception as e:
            logger.error(f"Error saving CSV: {e}")

    def save_json(self, filename: str = 'bloom_pharmacy_products.json'):
        """Save products to JSON file"""
        if not self.products:
            logger.warning("No products to save")
            return

        self.output_dir.mkdir(exist_ok=True)
        filepath = self.output_dir / filename

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.products, f, ensure_ascii=False, indent=2)

            logger.info(f"Saved {len(self.products)} products to {filepath}")

        except Exception as e:
            logger.error(f"Error saving JSON: {e}")

    @property
    def output_dir(self) -> Path:
        """Get output directory path"""
        return OUTPUT_DIR

def main():
    """Main execution"""
    logger.info("Starting Bloom Pharmacy Scraper")

    scraper = BloomPharmacyScraper(use_selenium=SELENIUM_AVAILABLE)

    try:
        # Scrape all categories (limit to 1 page per category for testing)
        # Remove max_pages_per_category to scrape all pages
        scraper.scrape_all(max_pages_per_category=1)

        # Save to files
        scraper.save_csv()
        scraper.save_json()

        logger.info(f"Total products scraped: {len(scraper.products)}")
        logger.info("Scraping completed!")

    finally:
        scraper.close()

if __name__ == "__main__":
    main()

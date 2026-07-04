import time
import csv
import json
import os
import random
import requests
import asyncio
from bs4 import BeautifulSoup
from googletrans import Translator
from chefaa_scraper.config import (
    DEFAULT_HEADERS, REQUEST_DELAY, REQUEST_TIMEOUT,
    MAX_RETRIES, BACKOFF_FACTOR, BASE_URL, LOCALE_PREFIX,
    CATEGORIES, DATA_DIR
)

# Initialize translator
translator = Translator()

def fetch_page(url):
    """
    Fetches a web page with retries, backoff, timeout, and polite rate-limiting.
    """
    # Sleep to respect rate limits
    time.sleep(REQUEST_DELAY + random.uniform(0.1, 0.5))

    retries = 0
    current_delay = REQUEST_DELAY

    while retries <= MAX_RETRIES:
        try:
            response = requests.get(url, headers=DEFAULT_HEADERS, timeout=REQUEST_TIMEOUT)
            if response.status_code == 200:
                return response.content, response.url
            elif response.status_code == 404:
                print(f"Page not found (404): {url}")
                return None, None
            else:
                print(f"HTTP Error {response.status_code} fetching: {url}")
        except requests.exceptions.RequestException as e:
            print(f"Request exception for {url}: {e}")
        
        retries += 1
        if retries <= MAX_RETRIES:
            wait_time = current_delay * BACKOFF_FACTOR
            print(f"Retrying ({retries}/{MAX_RETRIES}) in {wait_time}s...")
            time.sleep(wait_time)
            current_delay = wait_time

    print(f"Failed to fetch page after {MAX_RETRIES} retries: {url}")
    return None, None

def parse_category_products(html):
    """
    Parses product listings from a category page HTML.
    Returns a list of dictionaries containing product card metadata.
    """
    soup = BeautifulSoup(html, "html.parser")
    products = []
    
    # Locate all product containers
    product_cards = soup.find_all("div", class_="item")
    
    for card in product_cards:
        try:
            # 1. Product ID
            btn = card.find("button", class_="add_to_cart")
            product_id = btn.get("data-id") if btn else None
            
            # 2. Product Name/Title
            name_el = card.find(itemprop="name")
            name = name_el.get("content") if name_el else None
            if not name:
                h2 = card.find("h2")
                if h2:
                    name = h2.text.strip()
            
            # 3. Product Price
            price_el = card.find(itemprop="price")
            price = price_el.get("content") if price_el else None
            if not price:
                price_span = card.find("span", class_="m-0")
                if price_span:
                    price = price_span.text.strip()
                    
            # 4. Product Currency
            curr_el = card.find(itemprop="priceCurrency")
            currency = curr_el.get("content") if curr_el else "EGP"
            
            # 5. Detail Link
            link_el = card.find("a", class_="product_details_link")
            link = link_el.get("href") if link_el else None
            
            # 6. Thumbnail Image
            img_el = card.find("img")
            thumbnail = img_el.get("data-src") or img_el.get("src") if img_el else None
            
            if name or product_id:
                products.append({
                    "product_id": product_id,
                    "name": name,
                    "price": price,
                    "currency": currency,
                    "url": link,
                    "thumbnail_image": thumbnail
                })
        except Exception as e:
            print(f"Error parsing product card: {e}")
            
    return products

def parse_product_details(html):
    """
    Parses product page HTML to extract full details.
    """
    soup = BeautifulSoup(html, "html.parser")
    
    # 0. Try to get English name from page title or meta tags
    name_en = None
    title_tag = soup.find("title")
    if title_tag:
        title_text = title_tag.get_text()
        # Extract English part from title if available
        if " | " in title_text:
            parts = title_text.split(" | ")
            for part in parts:
                if all(ord(c) < 128 or c.isspace() for c in part if c not in ['-', '|']):
                    name_en = part.strip()
                    break
    
    # 1. Brand from metadata
    brand_el = soup.find("meta", attrs={"property": "product:brand"})
    brand = brand_el.get("content") if brand_el else None
    
    # 2. Category hierarchy from metadata
    category_el = soup.find("meta", attrs={"property": "product:product_type"})
    category = category_el.get("content") if category_el else None
    
    # 3. Availability from metadata
    avail_el = soup.find("meta", attrs={"property": "product:availability"})
    availability = avail_el.get("content") if avail_el else None
    
    # 4. Image gallery
    gallery_images = []
    gallery = soup.find(class_="product-gallery")
    if gallery:
        for img in gallery.find_all("img"):
            src = img.get("data-src") or img.get("src")
            if src and src not in gallery_images:
                gallery_images.append(src)
    if not gallery_images:
        # Fallback to og:image meta tags
        meta_imgs = soup.find_all("meta", attrs={"property": "og:image"})
        for m in meta_imgs:
            src = m.get("content")
            if src and src not in gallery_images:
                gallery_images.append(src)

    # 5. Overview and Specifications
    overview = ""
    specs = {}
    
    desc_container = soup.find(class_="description-product")
    if desc_container:
        tab_content = desc_container.find(class_="tab-content")
        if tab_content:
            panes = tab_content.find_all(class_="tab-pane")
            for i, pane in enumerate(panes):
                pane_text = pane.get_text("\n").strip()
                # Determine if it is specs pane or overview pane
                if "المواصفات" in pane_text or i == 1:
                    # Parse specifications table/list
                    spec_items = {}
                    # Try finding structured items (like brand, size)
                    for li in pane.find_all("li"):
                        text = li.text.strip()
                        if ":" in text:
                            parts = text.split(":", 1)
                            spec_items[parts[0].strip()] = parts[1].strip()
                        elif " " in text:
                            # Handle key-values without colons
                            parts = text.split("  ", 1)
                            if len(parts) == 2:
                                spec_items[parts[0].strip()] = parts[1].strip()
                            else:
                                spec_items[f"spec_{len(spec_items)}"] = text
                        else:
                            spec_items[f"spec_{len(spec_items)}"] = text
                    
                    for tr in pane.find_all("tr"):
                        tds = tr.find_all(["td", "th"])
                        if len(tds) == 2:
                            spec_items[tds[0].text.strip()] = tds[1].text.strip()
                            
                    if spec_items:
                        specs = spec_items
                    else:
                        specs = {"raw_specs": pane_text}
                else:
                    overview = pane_text
        else:
            overview = desc_container.get_text("\n").strip()
            
    return {
        "brand": brand,
        "category": category,
        "availability": availability,
        "gallery_images": gallery_images,
        "description": overview,
        "specifications": specs,
        "name_en": name_en
    }

def translate_to_english(text):
    """
    Translates Arabic text to English using Google Translate.
    Returns the translated text or original if translation fails.
    """
    if not text:
        return ""
    try:
        # Create a new event loop for this thread if none exists
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        result = loop.run_until_complete(translator.translate(text, src_language='ar', dest_language='en'))
        return result['text'] if isinstance(result, dict) and 'text' in result else (result.text if hasattr(result, 'text') else text)
    except Exception as e:
        return text

def extract_english_from_url(url):
    """
    Extracts English product name from product URL.
    URLs typically have format: /eg-ar/nowProduct/english-product-name-slug
    """
    if not url:
        return None
    try:
        # Extract the slug from the URL
        parts = url.rstrip('/').split('/')
        if len(parts) > 0:
            slug = parts[-1]
            # Convert slug to readable format (replace hyphens with spaces, remove IDs)
            words = slug.split('-')
            # Filter out short IDs and numbers
            english_words = [w for w in words if len(w) > 2 and not w.isdigit()]
            if english_words:
                return ' '.join(english_words)
    except:
        pass
    return None

def export_to_csv(data, filepath):
    """
    Exports a list of product dictionaries to a CSV file.
    Lists and dictionaries are serialized to clean strings.
    """
    if not data:
        print("No data to export.")
        return

    # Define CSV headers
    fieldnames = [
        "product_id",
        "name",
        "name_en",
        "price",
        "currency",
        "brand",
        "category",
        "availability",
        "url",
        "thumbnail_image",
        "gallery_images",
        "description",
        "specifications"
    ]

    try:
        with open(filepath, "w", newline="", encoding="utf-8-sig") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for item in data:
                # Prepare row values
                row = {
                    "product_id": item.get("product_id"),
                    "name": item.get("name"),
                    "name_en": item.get("name_en", ""),
                    "price": item.get("price"),
                    "currency": item.get("currency"),
                    "brand": item.get("brand"),
                    "category": item.get("category"),
                    "availability": item.get("availability"),
                    "url": item.get("url"),
                    "thumbnail_image": item.get("thumbnail_image"),
                }
                
                # Format gallery images as semicolon separated string
                gallery = item.get("gallery_images", [])
                row["gallery_images"] = ";".join(gallery) if isinstance(gallery, list) else gallery
                
                # Format description cleanly
                desc = item.get("description", "")
                row["description"] = desc.replace("\r", "").replace("\n", " ") if desc else ""
                
                # Format specifications as a semicolon separated key:value string
                specs = item.get("specifications", {})
                if isinstance(specs, dict):
                    specs_str = "; ".join([f"{k}: {v}" for k, v in specs.items()])
                else:
                    specs_str = str(specs).replace("\r", "").replace("\n", " ")
                row["specifications"] = specs_str
                
                writer.writerow(row)
        print(f"Exported {len(data)} items to CSV: {filepath}")
    except Exception as e:
        print(f"Error exporting to CSV {filepath}: {e}")

def export_to_json(data, filepath):
    """
    Exports product data directly to a JSON file.
    """
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Exported {len(data)} items to JSON: {filepath}")
    except Exception as e:
        print(f"Error exporting to JSON {filepath}: {e}")

def load_existing_product_ids(csv_filepath):
    """
    Loads product IDs that have already been scraped in the output CSV.
    This enables pausing and resuming scraping.
    """
    scraped_ids = set()
    if os.path.exists(csv_filepath):
        try:
            with open(csv_filepath, "r", encoding="utf-8-sig") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    pid = row.get("product_id")
                    if pid:
                        scraped_ids.add(pid)
        except Exception as e:
            print(f"Error reading existing CSV: {e}")
    return scraped_ids

def scrape_category(category_key, max_pages=None):
    """
    General category runner logic.
    Retrieves listing pages, extracts details, exports results to data/ directory.
    """
    if category_key not in CATEGORIES:
        print(f"Error: Category '{category_key}' is not defined in config.")
        return

    cat_config = CATEGORIES[category_key]
    category_name = cat_config["name_ar"]
    url_path = cat_config["url_path"]
    
    print(f"\n==================================================")
    print(f"Starting Scraper for Category: {category_name} ({category_key})")
    print(f"==================================================")
    
    csv_filepath = os.path.join(DATA_DIR, f"{category_key}.csv")
    json_filepath = os.path.join(DATA_DIR, f"{category_key}.json")
    
    # 1. Load existing results for resumes
    scraped_ids = load_existing_product_ids(csv_filepath)
    if scraped_ids:
        print(f"Found {len(scraped_ids)} existing scraped products in output CSV.")
        print("Resume mode active: Already scraped products will be skipped.")
    
    all_products = []
    
    # If resuming, load existing products into memory so we can save them back
    if os.path.exists(json_filepath):
        try:
            with open(json_filepath, "r", encoding="utf-8") as f:
                all_products = json.load(f)
                print(f"Loaded {len(all_products)} products from existing JSON file.")
        except Exception as e:
            print(f"Warning: Could not read existing JSON file: {e}")

    page = 1
    new_products_count = 0
    
    while True:
        if max_pages and page > max_pages:
            print(f"Reached page limit constraint ({max_pages}). Stopping.")
            break
            
        print(f"\n--- Scraping Page {page} ---")
        category_url = f"{BASE_URL}/{LOCALE_PREFIX}/{url_path}?page={page}"
        html, final_url = fetch_page(category_url)
        
        if not html:
            print("No HTML returned. Stopping category crawler.")
            break
            
        products_listing = parse_category_products(html)
        
        if not products_listing:
            print(f"No products found on page {page}. Scraping finished!")
            break
            
        print(f"Found {len(products_listing)} products listed on page {page}.")
        
        # Loop through products on this page and get full details
        for index, item in enumerate(products_listing):
            pid = item["product_id"]
            
            # Skip if already scraped
            if pid in scraped_ids:
                print(f" [{index+1}/{len(products_listing)}] Skipping ID {pid} (Already scraped)")
                continue
                
            detail_url = item["url"]
            if not detail_url:
                print(f" [{index+1}/{len(products_listing)}] ID {pid} has no detail URL. Skipping details.")
                all_products.append(item)
                scraped_ids.add(pid)
                new_products_count += 1
                continue
                
            print(f" [{index+1}/{len(products_listing)}] Fetching details for: {item['name'][:30]}... (ID: {pid})")
            
            # Check prefix for relative URLs
            full_detail_url = detail_url if detail_url.startswith("http") else f"{BASE_URL}{detail_url}"
            detail_html, _ = fetch_page(full_detail_url)
            
            if detail_html:
                details = parse_product_details(detail_html)
                # Merge page listing meta and full details
                item.update(details)
            else:
                print(f"  Warning: Failed to fetch product details for ID {pid}")
                # Keep card listing details if detail fetch fails
                item.update({
                    "brand": None,
                    "category": None,
                    "availability": None,
                    "gallery_images": [],
                    "description": "",
                    "specifications": {},
                    "name_en": None
                })
            
            # Add English translation of product name
            # Priority 1: Extract from product URL (most reliable)
            url_name = extract_english_from_url(item.get("url", ""))
            if url_name:
                item["name_en"] = url_name
                print(f"  ✓ Extracted from URL: {url_name[:40]}...")
            else:
                # Priority 2: Try page extraction or translation
                if item.get("name_en") and item["name_en"] != item.get("name"):
                    # name_en was extracted from page (not the Arabic name)
                    print(f"  ✓ Extracted from page: {item['name_en'][:40]}...")
                else:
                    # Priority 3: Use translation
                    product_name = item.get("name", "")
                    if product_name and product_name not in ["", None]:
                        item["name_en"] = translate_to_english(product_name)
                        if item["name_en"] != product_name:
                            print(f"  ✓ Translated: {item['name_en'][:40]}...")
                        else:
                            item["name_en"] = ""
                    else:
                        item["name_en"] = ""
            
            all_products.append(item)
            scraped_ids.add(pid)
            new_products_count += 1
            
            # Intermediate save every 5 new products to prevent data loss on crashes
            if new_products_count % 5 == 0:
                print(f"Saving progress... ({len(all_products)} total products)")
                export_to_csv(all_products, csv_filepath)
                export_to_json(all_products, json_filepath)
                
        page += 1
        
    # Final save of the complete database
    print(f"\nScraping complete for {category_name}!")
    print(f"Total products processed: {len(all_products)}")
    export_to_csv(all_products, csv_filepath)
    export_to_json(all_products, json_filepath)

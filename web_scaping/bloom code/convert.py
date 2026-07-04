import json
import csv
import os

json_file = r'bloom_pharmacy_data\bloom_ALL_products.json'
csv_file = r'bloom_pharmacy_data\bloom_ALL_products_final.csv'

try:
    print(f"Reading {json_file}...")
    with open(json_file, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    if products:
        # Collect all unique keys across all dictionaries to be safe
        fieldnames = set()
        for p in products:
            fieldnames.update(p.keys())
        fieldnames = list(fieldnames)
        
        # Optionally reorder fieldnames to have the most important first
        priority = ['id', 'url', 'name_en', 'name_ar', 'description_en', 'description_ar', 'price', 'compare_at_price', 'discount_pct', 'currency', 'categories_en', 'categories_ar', 'vendor', 'brand', 'image_url', 'barcode', 'sku']
        ordered_fieldnames = [f for f in priority if f in fieldnames] + [f for f in fieldnames if f not in priority]
        
        print(f"Writing {csv_file}...")
        with open(csv_file, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=ordered_fieldnames)
            writer.writeheader()
            writer.writerows(products)
            
        print("Conversion successful.")
    else:
        print("No products found in JSON.")
except Exception as e:
    print(f"Error: {e}")

import os

# Base configurations
BASE_URL = "https://chefaa.com"
LOCALE_PREFIX = "eg-ar"  # Default Egypt (Arabic) region

# Output Directory configurations
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Create data output directory if it doesn't exist
os.makedirs(DATA_DIR, exist_ok=True)

# Rate Limiting & Robustness
REQUEST_DELAY = 1.5      # Delay in seconds between requests to avoid overloading/banning
REQUEST_TIMEOUT = 15      # Max seconds to wait for page response
MAX_RETRIES = 3           # Number of attempts for failed HTTP requests
BACKOFF_FACTOR = 2        # Factor to multiply delay by on failure retries

# HTTP Request Headers to simulate a real browser browser request
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "ar,en-US;q=0.9,en;q=0.8",
    "Referer": "https://chefaa.com/",
    "Connection": "keep-alive"
}

# Category Configurations
# Maps a category identifier to its respective URL path segment on Chefaa
CATEGORIES = {
    "medications": {
        "name_ar": "الأدوية",
        "url_path": "now/category/medications"
    },
    "hair_care": {
        "name_ar": "العناية بالشعر",
        "url_path": "now/category/hair-care"
    },
    "skin_care": {
        "name_ar": "العناية بالبشرة",
        "url_path": "now/category/skin-care"
    },
    "daily_essentials": {
        "name_ar": "العناية اليومية",
        "url_path": "now/category/daily-essentials"
    },
    "mom_baby": {
        "name_ar": "الأم والطفل",
        "url_path": "now/category/mom-baby"
    },
    "makeup_accessories": {
        "name_ar": "المكياج والاكسسوارات",
        "url_path": "now/category/makeup-accessories"
    },
    "health_care_devices": {
        "name_ar": "المستلزمات الطبية",
        "url_path": "now/category/health-care-devices"
    },
    "vitamins_supplements": {
        "name_ar": "الفيتامينات والمكملات",
        "url_path": "now/category/vitamins-supplements"
    },
    "sexual_wellness": {
        "name_ar": "الصحة الجنسية",
        "url_path": "now/category/sexual-welness"
    }
}

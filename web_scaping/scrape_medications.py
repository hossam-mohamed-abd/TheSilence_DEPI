import os
import sys

# Add parent directory to sys.path to allow execution from any current working directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chefaa_scraper.scraper_base import scrape_category

if __name__ == "__main__":
    # Scrapes all pages of the medications category
    scrape_category("medications")

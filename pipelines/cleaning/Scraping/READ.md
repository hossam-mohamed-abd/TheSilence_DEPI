Here is a clean, concise, and straight-to-the-point `README.md` entirely in English:

---

# Arab Countries Cities Scraper

Python scripts to scrape city and region data for Egypt and Saudi Arabia from Wikipedia and save them as clean CSV files.

## 🚀 Features

* Handles complex Wikipedia table layouts (like rowspans/colspans in the Saudi data).


* Automatically cleans text, removes duplicates, and exports with `utf-8-sig` encoding for flawless Excel compatibility.



## 📁 Project Structure

* `Scraping Egypt cities.py`: Extracts Egyptian governorates and cities into `egypt_cities.csv`.


* `Scraping Saudi cities.py`: Extracts Saudi regions and cities into `saudi_regions_cities.csv`.



## 💻 Setup & Usage

### 1. Install dependencies

```bash
pip install requests beautifulsoup4 pandas lxml

```

### 2. Run the scrapers

```bash
python "Scraping Egypt cities.py"
python "Scraping Saudi cities.py"

```

## 📊 Output Preview

### Egypt Data

| المحافظة (Governorate) | المدينة (City) |
| --- | --- |
| القاهرة | القاهرة |

### Saudi Arabia Data

| المنطقة (Region) | المحافظة/المدينة (City/Governorate) |
| --- | --- |
| منطقة الرياض | الدرعية |

---

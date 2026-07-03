# -*- coding: utf-8 -*-
"""
سكرابينج صفحة ويكيبيديا: قائمة محافظات السعودية
الناتج: ملف CSV فيه عمودين -> المنطقة | المحافظة/المدينة
"""

import requests
from bs4 import BeautifulSoup
import csv

URL = "https://ar.wikipedia.org/wiki/قائمة_محافظات_السعودية"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; scraper/1.0)"}


def get_cell_text(cell):
    return cell.get_text(strip=True)


def build_grid(rows):
    """
    يحول صفوف الجدول (tr) لـ grid كامل (لستة من لستات)، بيراعي rowspan و colspan
    (اللي بيتكرر هنا لعدة أعمدة زي: الكثافة السكانية / المساحة الكلية / إجمالي السكان / المنطقة)،
    بحيث كل صف يبقى بنفس عدد أعمدة الهيدر تماماً.
    """
    grid = []
    pending = {}  # column_index -> [remaining_rows, text]

    for row in rows:
        cells = row.find_all(["td", "th"])
        cell_iter = iter(cells)
        current_row = []
        col = 0

        while True:
            if col in pending and pending[col][0] > 0:
                current_row.append(pending[col][1])
                pending[col][0] -= 1
                if pending[col][0] == 0:
                    del pending[col]
                col += 1
                continue

            cell = next(cell_iter, None)
            if cell is None:
                break

            text = get_cell_text(cell)
            colspan = int(cell.get("colspan", 1) or 1)
            rowspan = int(cell.get("rowspan", 1) or 1)

            for _ in range(colspan):
                current_row.append(text)
                if rowspan > 1:
                    pending[col] = [rowspan - 1, text]
                col += 1

        grid.append(current_row)

    return grid


def parse_table(table):
    """
    يرجع لستة من (region, city) لكل جدول باستخدام grid كامل يراعي rowspan/colspan.
    """
    rows = table.find_all("tr")
    if not rows:
        return []

    grid = build_grid(rows)
    if len(grid) < 2:
        return []

    headers_text = grid[0]

    city_idx = None
    region_idx = None
    for i, h in enumerate(headers_text):
        if "المحافظات" in h and city_idx is None:
            city_idx = i
        if h == "المنطقة" or h.startswith("المنطقة"):
            region_idx = i

    if city_idx is None:
        return []  # مش الجدول اللي إحنا عايزينه

    results = []
    for data_row in grid[1:]:
        if city_idx >= len(data_row):
            continue
        city = data_row[city_idx]
        region = data_row[region_idx] if region_idx is not None and region_idx < len(data_row) else None
        if city and region:
            results.append((region, city))

    return results


def main():
    resp = requests.get(URL, headers=HEADERS, timeout=30)
    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, "lxml")

    tables = soup.find_all("table", {"class": "wikitable"})

    all_results = []
    for table in tables:
        all_results.extend(parse_table(table))

    # شيل أي تكرار لو حصل
    seen = set()
    final_results = []
    for region, city in all_results:
        key = (region, city)
        if key not in seen:
            seen.add(key)
            final_results.append(key)

    out_file = "saudi_regions_cities.csv"
    with open(out_file, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["المنطقة", "المحافظة/المدينة"])
        writer.writerows(final_results)

    print(f"تم استخراج {len(final_results)} صف، وحفظهم في {out_file}")

    # طباعة أول 15 صف كمعاينة سريعة
    for r in final_results[:15]:
        print(r)


if __name__ == "__main__":
    main()

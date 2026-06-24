#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scraper لمنتجات متجر Al Dawaa Pharmacies (Shopify) - aldawaaegy.com

الفكرة:
  1) نجيب كل روابط المنتجات من صفحة الكولكشن (مع التعامل مع pagination تلقائيًا).
  2) لكل منتج، نستخدم endpoint الرسمي بتاع Shopify:  /products/<handle>.js
     وده بيرجع JSON كامل وموثوق فيه: الاسم، السعر، التوفر، الصور، الوصف (HTML)،
     البراند (vendor)، الـ variants، tags... إلخ. ده أفضل وأضمن من تحليل HTML.
  3) كمان نجيب من صفحة المنتج نفسها الـ breadcrumb (التصنيف/category) والـ
     specifications لو موجودة فعليًا في الصفحة (لأنها مش موجودة في JSON الرسمي).
  4) نخرّج النتيجة CSV + JSON + ملف Markdown منسق.

الاستخدام:
    python scrape_aldawaa.py --collection men-care-1 --max-pages 0
    python scrape_aldawaa.py --url "https://aldawaaegy.com/ar/collections/men-care-1"

ملاحظات:
  - الكود بيحترم تأخير بسيط بين الطلبات (rate limiting) حتى لا يثقل على السيرفر.
  - لو حصل خطأ شبكة في منتج معين، بيتم تسجيله والاستمرار في باقي المنتجات.
  - لا يحتاج إلى تثبيت lxml (يستخدم html.parser المدمج).
"""

import argparse
import csv
import json
import re
import sys
import time
from html import unescape
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

# ========== الإعدادات الأساسية ==========
BASE_DOMAIN = "https://aldawaaegy.com"
DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ar,en;q=0.8",
}
REQUEST_DELAY = 0.6  # ثانية بين كل طلب وطلب (rate limiting لطيف)
PARSER = "html.parser"  # استخدم html.parser بدلاً من lxml لتجنب التبعيات الإضافية


# ========== دوال مساعدة ==========
def fetch(url, session, retries=3, timeout=20):
    """طلب HTTP مع إعادة محاولة بسيطة."""
    last_err = None
    for attempt in range(1, retries + 1):
        try:
            resp = session.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
            resp.raise_for_status()
            return resp
        except requests.RequestException as e:
            last_err = e
            time.sleep(1.0 * attempt)
    print(f"[تحذير] فشل تحميل {url} بعد {retries} محاولات: {last_err}", file=sys.stderr)
    return None


def normalize_collection_url(raw_url_or_handle):
    """
    يقبل:
      - handle بسيط مثل: men-care-1
      - رابط كامل مثل: https://aldawaaegy.com/ar/collections/men-care-1
    ويرجع رابط الكولكشن الكامل (بدون باراميترات صفحة).
    """
    if raw_url_or_handle.startswith("http"):
        parsed = urlparse(raw_url_or_handle)
        path = parsed.path.rstrip("/")
        return f"{BASE_DOMAIN}{path}"
    handle = raw_url_or_handle.strip("/")
    return f"{BASE_DOMAIN}/ar/collections/{handle}"


def collect_product_urls(collection_url, session, max_pages=0):
    """
    يمر على صفحات الكولكشن (?page=1, 2, 3 ...) ويجمع روابط المنتجات الفريدة.
    max_pages = 0 يعني: استمر حتى لا توجد منتجات جديدة (تلقائي بالكامل).
    """
    product_urls = []
    seen = set()
    page = 1

    while True:
        page_url = f"{collection_url}?page={page}"
        print(f"[..] تحميل صفحة الكولكشن: {page_url}")
        resp = fetch(page_url, session)
        if resp is None:
            break

        soup = BeautifulSoup(resp.text, PARSER)
        # روابط المنتجات بتبقى عادة على شكل /ar/.../products/<handle>
        links = soup.select('a[href*="/products/"]')
        page_handles = set()
        for a in links:
            href = a.get("href", "")
            if "/products/" not in href:
                continue
            full = urljoin(BASE_DOMAIN, href.split("?")[0])
            # استخراج الـ handle بتاع المنتج لإزالة التكرار حتى لو الروابط فيها بريفكسات مختلفة
            handle = full.rstrip("/").split("/products/")[-1]
            if handle not in seen:
                seen.add(handle)
                page_handles.add(handle)
                product_urls.append((handle, full))

        print(f"    -> منتجات جديدة في هذه الصفحة: {len(page_handles)}")

        if len(page_handles) == 0:
            # لا منتجات جديدة = انتهت الصفحات
            break

        if max_pages and page >= max_pages:
            break

        page += 1
        time.sleep(REQUEST_DELAY)

    return product_urls


def get_product_json(handle, session):
    """يجيب JSON الرسمي للمنتج من endpoint بتاع شوبيفاي: /products/<handle>.js"""
    url = f"{BASE_DOMAIN}/products/{handle}.js"
    resp = fetch(url, session)
    if resp is None:
        return None
    try:
        return resp.json()
    except json.JSONDecodeError:
        print(f"[تحذير] رد غير صالح JSON للمنتج: {handle}", file=sys.stderr)
        return None


def clean_html_to_text(html_content):
    """يحول وصف HTML إلى نص نظيف بدون تاجات."""
    if not html_content:
        return ""
    soup = BeautifulSoup(html_content, PARSER)
    text = soup.get_text(separator=" ", strip=True)
    text = re.sub(r"\s+", " ", text).strip()
    return unescape(text)


def extract_breadcrumb_category(product_page_url, session):
    """
    يحاول استخراج مسار التصنيف (breadcrumb) من صفحة المنتج نفسها،
    لأن هذا غير متوفر في /products/<handle>.js
    يرجع نص مثل: "الرئيسية > رعاية الرجال > ..." لو موجود، أو فاضي لو غير متاح.
    """
    resp = fetch(product_page_url, session)
    if resp is None:
        return ""
    soup = BeautifulSoup(resp.text, PARSER)

    # محاولة 1: breadcrumb عام (selectors شائعة في ثيمات Shopify)
    candidates = soup.select(
        ".breadcrumb, .breadcrumbs, nav.breadcrumb, [class*='breadcrumb'] a, "
        "[class*='breadcrumb'] span"
    )
    parts = []
    for el in candidates:
        txt = el.get_text(strip=True)
        if txt and txt not in parts:
            parts.append(txt)
    if parts:
        return " > ".join(parts)

    # محاولة 2: من JSON-LD لو موجود (BreadcrumbList)
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script.string or "{}")
        except (json.JSONDecodeError, TypeError):
            continue
        items = data.get("itemListElement") if isinstance(data, dict) else None
        if items:
            names = [it.get("name", "") for it in items if isinstance(it, dict)]
            names = [n for n in names if n]
            if names:
                return " > ".join(names)

    return ""


def extract_specifications(product_page_url, session):
    """
    يحاول استخراج جدول/قائمة "specifications" أو "المواصفات" من صفحة المنتج،
    لأنها غير متوفرة في JSON الرسمي. يرجع قائمة "key: value".
    """
    resp = fetch(product_page_url, session)
    if resp is None:
        return []
    soup = BeautifulSoup(resp.text, PARSER)
    specs = []

    # محاولة 1: جداول specs (table rows مع th/td)
    for table in soup.select("table"):
        for row in table.select("tr"):
            cells = row.find_all(["th", "td"])
            if len(cells) >= 2:
                key = cells[0].get_text(strip=True)
                val = cells[1].get_text(strip=True)
                if key and val:
                    specs.append(f"{key}: {val}")

    # محاولة 2: قوائم تعريف dl/dt/dd
    for dl in soup.select("dl"):
        dts = dl.find_all("dt")
        dds = dl.find_all("dd")
        for dt, dd in zip(dts, dds):
            key = dt.get_text(strip=True)
            val = dd.get_text(strip=True)
            if key and val:
                specs.append(f"{key}: {val}")

    # إزالة أي تكرار مع الحفاظ على الترتيب
    seen = set()
    unique_specs = []
    for s in specs:
        if s not in seen:
            seen.add(s)
            unique_specs.append(s)
    return unique_specs


def build_product_record(handle, product_url, session, fetch_extra=True):
    """يبني سجل المنتج الكامل بكل الحقول المطلوبة."""
    data = get_product_json(handle, session)
    if data is None:
        return None

    product_id = data.get("id")
    name = data.get("title", "").strip()
    vendor = data.get("vendor", "").strip()

    variants = data.get("variants", [])
    first_variant = variants[0] if variants else {}

    # السعر: بيرجع بالـ cents في JSON الرسمي لشوبيفاي
    price_cents = first_variant.get("price")
    price = round(price_cents / 100, 2) if isinstance(price_cents, (int, float)) else None

    currency = "EGP"  # المتجر يستخدم الجنيه المصري كما يظهر في الصفحة (EGP)

    # التوفر: نعتمد على available في JSON (true/false) + نص "in stock"/"sold out"
    available = data.get("available", False)
    if not available:
        availability = "sold out"
    else:
        availability = "in stock"

    # الصور
    images = data.get("images", []) or []
    images = [urljoin("https:", img) if img.startswith("//") else img for img in images]
    thumbnail_image = images[0] if images else ""
    gallery_images = ";".join(images)

    description = clean_html_to_text(data.get("body_html", ""))

    record = {
        "product_id": product_id,
        "name": name,
        "price": price,
        "currency": currency,
        "brand": vendor,
        "category": "",
        "availability": availability,
        "url": product_url,
        "thumbnail_image": thumbnail_image,
        "gallery_images": gallery_images,
        "description": description,
        "specifications": "",
    }

    if fetch_extra:
        time.sleep(REQUEST_DELAY)
        record["category"] = extract_breadcrumb_category(product_url, session)
        time.sleep(REQUEST_DELAY)
        specs = extract_specifications(product_url, session)
        record["specifications"] = ";".join(specs)

    return record


def save_csv(records, path):
    fieldnames = [
        "product_id", "name", "price", "currency", "brand", "category",
        "availability", "url", "thumbnail_image", "gallery_images",
        "description", "specifications",
    ]
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in records:
            writer.writerow(r)


def save_json(records, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


def save_markdown(records, path, collection_url):
    lines = []
    lines.append(f"# منتجات: {collection_url}")
    lines.append("")
    lines.append(f"عدد المنتجات: {len(records)}")
    lines.append("")
    for r in records:
        lines.append(f"## {r['name']}")
        lines.append("")
        if r["thumbnail_image"]:
            lines.append(f"![{r['name']}]({r['thumbnail_image']})")
            lines.append("")
        lines.append(f"- **رقم المنتج (ID):** {r['product_id']}")
        lines.append(f"- **السعر:** {r['price']} {r['currency']}")
        lines.append(f"- **البراند:** {r['brand'] or '-'}")
        lines.append(f"- **التصنيف:** {r['category'] or '-'}")
        lines.append(f"- **التوفر:** {r['availability']}")
        lines.append(f"- **الرابط:** {r['url']}")
        if r["gallery_images"]:
            imgs = r["gallery_images"].split(";")
            lines.append(f"- **عدد صور المعرض:** {len(imgs)}")
        if r["specifications"]:
            lines.append(f"- **المواصفات:**")
            for spec in r["specifications"].split(";"):
                lines.append(f"  - {spec}")
        if r["description"]:
            desc_preview = r["description"][:300]
            lines.append("")
            lines.append(f"**الوصف:** {desc_preview}{'...' if len(r['description']) > 300 else ''}")
        lines.append("")
        lines.append("---")
        lines.append("")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    parser = argparse.ArgumentParser(description="Scraper لمنتجات متجر aldawaaegy.com (Shopify)")
    parser.add_argument(
        "--collection", default="2025-offers",
        help="اسم (handle) الكولكشن، مثل: men-care-1"
    )
    parser.add_argument(
        "--url", default=None,
        help="رابط كامل لصفحة الكولكشن (لو موجود، يتجاوز --collection)"
    )
    parser.add_argument(
        "--max-pages", type=int, default=0,
        help="أقصى عدد صفحات يتم تصفحها (0 = تلقائي حتى النهاية)"
    )
    parser.add_argument(
        "--no-extra", action="store_true",
        help="عدم جلب category/specifications من صفحة المنتج (أسرع، لكن بدون هذه الحقول)"
    )
    parser.add_argument(
        "--limit", type=int, default=0,
        help="حد أقصى لعدد المنتجات المراد سحبها (0 = الكل) - مفيد للتجربة السريعة"
    )
    parser.add_argument(
        "--out-prefix", default="./aldawaa_products",
        help="بريفكس مسار ملفات الخروج (بدون امتداد) - مثال: ./output/aldawaa"
    )
    args = parser.parse_args()

    # التأكد من وجود مجلد الإخراج إذا كان المسار يتضمن مجلدات
    out_dir = os.path.dirname(args.out_prefix)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    collection_url = normalize_collection_url(args.url or args.collection)
    print(f"== رابط الكولكشن: {collection_url}")

    session = requests.Session()

    product_pairs = collect_product_urls(collection_url, session, max_pages=args.max_pages)
    print(f"== إجمالي روابط المنتجات المكتشفة: {len(product_pairs)}")

    if args.limit:
        product_pairs = product_pairs[: args.limit]
        print(f"== (تم تحديد الحد الأقصى للتجربة: {len(product_pairs)} منتج)")

    records = []
    for i, (handle, full_url) in enumerate(product_pairs, start=1):
        print(f"[{i}/{len(product_pairs)}] جاري سحب: {handle}")
        rec = build_product_record(
            handle, full_url, session, fetch_extra=not args.no_extra
        )
        if rec:
            records.append(rec)
        time.sleep(REQUEST_DELAY)

    print(f"== تم سحب {len(records)} منتج بنجاح من أصل {len(product_pairs)}")

    csv_path = f"{args.out_prefix}.csv"
    json_path = f"{args.out_prefix}.json"
    md_path = f"{args.out_prefix}.md"

    save_csv(records, csv_path)
    save_json(records, json_path)
    save_markdown(records, md_path, collection_url)

    print(f"== تم الحفظ في:\n  - {csv_path}\n  - {json_path}\n  - {md_path}")


if __name__ == "__main__":
    # إضافة import os لاستخدامه في إنشاء المجلدات
    import os
    main()
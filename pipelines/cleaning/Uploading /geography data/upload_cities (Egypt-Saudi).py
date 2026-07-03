import psycopg2
import psycopg2.extras
from psycopg2.extras import execute_values
import pandas as pd
import os

# ── Database Connection ───────────────────────────────────────
DATABASE_URL = "postgresql://neondb_owner:npg_Gi2nkbKme4gx@ep-spring-sound-atfc1f55-pooler.c-9.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()
print("✅ Connected to database!\n")

# ── File Path ─────────────────────────────────────────────────
folder = os.path.dirname(os.path.abspath(__file__))

# ══════════════════════════════════════════════════════════════
# Arabic governorate name → governorate_id (from governorates table)
# Egypt  country_id = 62  |  Saudi Arabia country_id = 189
# ══════════════════════════════════════════════════════════════
GOV_MAP = {
    # ── Egypt ─────────────────────────────────────────────────
    "محافظة القاهرة":        821,
    "محافظة الجيزة":         817,
    "محافظة القليوبية":      820,
    "محافظة الإسكندرية":     815,
    "محافظة البحيرة":        812,
    "محافظة مطروح":          833,
    "محافظة دمياط":          830,
    "محافظة الدقهلية":       810,
    "محافظة كفر الشيخ":      832,
    "محافظة الغربية":        814,
    "محافظة المنوفية":       819,
    "محافظة الشرقية":        825,
    "محافظة بورسعيد":        829,
    "محافظة الإسماعيلية":    816,
    "محافظة السويس":         824,
    "محافظة شمال سيناء":     835,
    "محافظة جنوب سيناء":     831,
    "محافظة بني سويف":       828,
    "محافظة الفيوم":         813,
    "محافظة المنيا":         818,
    "محافظة أسيوط":          827,
    "محافظة الوادي الجديد":  823,
    "محافظة البحر الأحمر":   811,
    "محافظة سوهاج":          836,
    "محافظة قنا":            834,
    "محافظة الأقصر":         822,
    "محافظة أسوان":          826,
    # ── Saudi Arabia ──────────────────────────────────────────
    "منطقة الرياض":              2699,
    "منطقة مكة المكرمة":         2702,
    "منطقة المدينة المنورة":      2696,
    "منطقة القصيم":              2697,
    "المنطقة الشرقية":           2700,
    "منطقة عسير":                2706,
    "منطقة تبوك":                2704,
    "منطقة حائل":                2705,
    "منطقة الحدود الشمالية":     2698,
    "منطقة جازان":               2701,
    "منطقة نجران":               2703,
    "منطقة الباحة":              2694,
    "منطقة الجوف":               2695,
}

# ══════════════════════════════════════════════════════════════
# cities
# ══════════════════════════════════════════════════════════════
print("🏙️ Uploading cities...")

df = pd.read_excel(os.path.join(folder, "Egy-Sau Cities.xlsx"))

# Map Arabic governorate name → governorate_id
df["governorate_id"] = df["المحافظة"].map(GOV_MAP)

# Check for any unmapped rows
unmapped = df[df["governorate_id"].isna()]
if not unmapped.empty:
    print(f"  ⚠️  Warning: {len(unmapped)} rows could not be mapped:")
    print(unmapped["المحافظة"].unique())

# Drop unmapped rows and assign auto-increment IDs
df = df.dropna(subset=["governorate_id"]).reset_index(drop=True)
df["id"] = df.index + 1

batch = []
for _, row in df.iterrows():
    batch.append((
        int(row["id"]),
        int(row["governorate_id"]),
        str(row["المدينة"]),
    ))

execute_values(cursor, """
    INSERT INTO cities (id, governorate_id, name)
    VALUES %s
    ON CONFLICT (id) DO NOTHING
""", batch, page_size=500)

conn.commit()
print(f"  ✅ Uploaded {len(df)} rows\n")

# ── Close Connection ──────────────────────────────────────────
cursor.close()
conn.close()
print("🎉 Cities uploaded successfully!")

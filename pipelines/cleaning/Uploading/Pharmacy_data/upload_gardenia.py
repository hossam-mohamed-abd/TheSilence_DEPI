import psycopg2
from psycopg2.extras import execute_values
import pandas as pd
import os

# ── الاتصال بالداتابيز ──────────────────────────────────────
DATABASE_URL = "postgresql://neondb_owner:npg_Gi2nkbKme4gx@ep-spring-sound-atfc1f55-pooler.c-9.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()
print("✅ اتصلنا بالداتابيز بنجاح!\n")

# ── مسار ملفات output_updated ────────────────────────────────
# غيّر المسار ده لو output_updated في مكان تاني
folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_updated")

# ══════════════════════════════════════════════════════════════
# 1. drug_categories — بس الجديدة (لو فيه)
# ══════════════════════════════════════════════════════════════
print("📦 بيرفع drug_categories الجديدة...")

df_new  = pd.read_csv(os.path.join(folder,                        "drug_categories.csv"))
df_old  = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "output", "drug_categories.csv"))

new_only = df_new[~df_new["id"].isin(df_old["id"])].copy()
new_only = new_only.where(pd.notnull(new_only), None)

if new_only.empty:
    print("  ℹ️  مفيش categories جديدة\n")
else:
    for _, row in new_only.iterrows():
        cursor.execute("""
            INSERT INTO drug_categories (id, name, description, created_at)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """, (row["id"], row["name"], row["description"], row["created_at"]))
    conn.commit()
    print(f"  ✅ تم رفع {len(new_only)} category جديدة\n")

# ══════════════════════════════════════════════════════════════
# 2. pharmacies — بس Gardenia (id=4)
# ══════════════════════════════════════════════════════════════
print("🏪 بيرفع Gardenia في pharmacies...")

df_pharma = pd.read_csv(os.path.join(folder, "pharmacies.csv"))
gardenia  = df_pharma[df_pharma["id"] == 4].copy()
gardenia  = gardenia.where(pd.notnull(gardenia), None)

for _, row in gardenia.iterrows():
    cursor.execute("""
        INSERT INTO pharmacies (id, name, phone, email, address, is_active, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING
    """, (row["id"], row["name"], row["phone"], row["email"],
          row["address"], row["is_active"], row["created_at"]))

conn.commit()
print(f"  ✅ Gardenia اتضافت (pharmacy_id = 4)\n")

# ══════════════════════════════════════════════════════════════
# 3. drugs — بس الجديدة من Gardenia (id > 11199)
# ══════════════════════════════════════════════════════════════
print("💊 بيرفع drugs الجديدة... (هياخد شوية وقت)")

df_drugs_new = pd.read_csv(os.path.join(folder, "drugs.csv"))
df_drugs_old = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "output", "drugs.csv"))

new_drugs = df_drugs_new[~df_drugs_new["id"].isin(df_drugs_old["id"])].copy()
new_drugs = new_drugs.where(pd.notnull(new_drugs), None)

print(f"  عدد الأدوية الجديدة: {len(new_drugs):,}")

batch = []
for _, row in new_drugs.iterrows():
    batch.append((
        row["id"], row["category_id"], row["name"], row["active_substance"],
        row["dosage_form"], row["strength"], row["manufacturer"],
        row["description"], row["image_url"], row["created_at"], row["updated_at"]
    ))

if batch:
    execute_values(cursor, """
        INSERT INTO drugs (id, category_id, name, active_substance, dosage_form,
                           strength, manufacturer, description, image_url,
                           created_at, updated_at)
        VALUES %s
        ON CONFLICT (id) DO NOTHING
    """, batch, page_size=500)
    conn.commit()
    print(f"  ✅ تم رفع {len(new_drugs):,} دواء جديد\n")
else:
    print("  ℹ️  مفيش أدوية جديدة\n")

# ══════════════════════════════════════════════════════════════
# 4. pharmacy_inventory — بس صفوف Gardenia الجديدة
# ══════════════════════════════════════════════════════════════
print("🏥 بيرفع pharmacy_inventory لـ Gardenia... (هياخد شوية وقت)")

df_inv_new = pd.read_csv(os.path.join(folder, "pharmacy_inventory.csv"))
df_inv_old = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "output", "pharmacy_inventory.csv"))

new_inv = df_inv_new[~df_inv_new["id"].isin(df_inv_old["id"])].copy()
new_inv = new_inv.where(pd.notnull(new_inv), None)

print(f"  عدد صفوف الـ inventory الجديدة: {len(new_inv):,}")

batch = []
for _, row in new_inv.iterrows():
    batch.append((
        row["id"], row["pharmacy_id"], row["drug_id"], row["quantity"],
        row["minimum_stock"], row["price"], row["last_updated"]
    ))

if batch:
    execute_values(cursor, """
        INSERT INTO pharmacy_inventory (id, pharmacy_id, drug_id, quantity,
                                        minimum_stock, price, last_updated)
        VALUES %s
        ON CONFLICT (id) DO NOTHING
    """, batch, page_size=500)
    conn.commit()
    print(f"  ✅ تم رفع {len(new_inv):,} صف جديد\n")
else:
    print("  ℹ️  مفيش inventory جديد\n")

# ── إغلاق الاتصال ────────────────────────────────────────────
cursor.close()
conn.close()
print("🎉 كل بيانات Gardenia اتحملت على الداتابيز بنجاح!")

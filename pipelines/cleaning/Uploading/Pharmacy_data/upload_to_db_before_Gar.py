import psycopg2
import psycopg2.extras
from psycopg2.extras import execute_values
import pandas as pd
import os

# ── الاتصال بالداتابيز ──────────────────────────────────────
DATABASE_URL = "postgresql://neondb_owner:npg_Gi2nkbKme4gx@ep-spring-sound-atfc1f55-pooler.c-9.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()
print("✅ اتصلنا بالداتابيز بنجاح!\n")

# ── مسار الملفات ─────────────────────────────────────────────
folder = os.path.dirname(os.path.abspath(__file__))
# ══════════════════════════════════════════════════════════════
# 1. drug_categories
# ══════════════════════════════════════════════════════════════
print("📦 بيرفع drug_categories...")

df = pd.read_csv(os.path.join(folder, "drug_categories.csv"))
df = df.where(pd.notnull(df), None)

for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO drug_categories (id, name, description, created_at)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING
    """, (row["id"], row["name"], row["description"], row["created_at"]))

conn.commit()
print(f"  ✅ تم رفع {len(df)} صف\n")

# ══════════════════════════════════════════════════════════════
# 2. drugs
# ══════════════════════════════════════════════════════════════
print("💊 بيرفع drugs... (هياخد شوية وقت)")

df = pd.read_csv(os.path.join(folder, "drugs.csv"))
df = df.where(pd.notnull(df), None)

text_columns = ["name", "active_substance", "dosage_form", "strength", "manufacturer", "image_url"]
for col in text_columns:
    if col in df.columns:
        max_len = df[col].dropna().apply(len).max()
        print(f"{col}: max length = {max_len}")

batch = []
for _, row in df.iterrows():
    batch.append((
        row["id"], row["category_id"], row["name"], row["active_substance"],
        row["dosage_form"], row["strength"], row["manufacturer"],
        row["description"], row["image_url"], row["created_at"], row["updated_at"]
    ))

execute_values(cursor, """
    INSERT INTO drugs (id, category_id, name, active_substance, dosage_form,
                       strength, manufacturer, description, image_url, created_at, updated_at)
    VALUES %s
    ON CONFLICT (id) DO NOTHING
""", batch, page_size=500)

conn.commit()
print(f"  ✅ تم رفع {len(df)} صف\n")

# ══════════════════════════════════════════════════════════════
# 3. pharmacies  
# ══════════════════════════════════════════════════════════════
print("🏪 بيرفع pharmacies...")

df = pd.read_csv(os.path.join(folder, "pharmacies.csv"))
df = df.where(pd.notnull(df), None)

batch = []
for _, row in df.iterrows():
    batch.append((
        row["id"], row["name"], row["phone"], row["email"], row["address"],
         row["is_active"],
        row["created_at"]
    ))

execute_values(cursor, """
    INSERT INTO pharmacies (id, name, phone, email, address,
                             is_active, created_at)
    VALUES %s
    ON CONFLICT (id) DO NOTHING
""", batch, page_size=500)

conn.commit()
print(f"  ✅ تم رفع {len(df)} صف\n")

# ══════════════════════════════════════════════════════════════
# 4. pharmacy_inventory
# ══════════════════════════════════════════════════════════════
print("🏥 بيرفع pharmacy_inventory... (هياخد شوية وقت)")

df = pd.read_csv(os.path.join(folder, "pharmacy_inventory.csv"))
df = df.where(pd.notnull(df), None)

batch = []
for _, row in df.iterrows():
    batch.append((
        row["id"], row["pharmacy_id"], row["drug_id"], row["quantity"],
        row["minimum_stock"], row["price"], row["last_updated"]
    ))

execute_values(cursor, """
    INSERT INTO pharmacy_inventory (id, pharmacy_id, drug_id, quantity,
                                    minimum_stock, price, last_updated)
    VALUES %s
    ON CONFLICT (id) DO NOTHING
""", batch, page_size=500)

conn.commit()
print(f"  ✅ تم رفع {len(df)} صف\n")


# ── إغلاق الاتصال ────────────────────────────────────────────
cursor.close()
conn.close()
print("🎉 كل الداتا اتحملت على الداتابيز بنجاح!")
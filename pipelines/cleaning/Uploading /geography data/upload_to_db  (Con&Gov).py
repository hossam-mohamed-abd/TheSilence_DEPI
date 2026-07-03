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
# countries
# ══════════════════════════════════════════════════════════════
print("🌍 بيرفع countries...")

df = pd.read_csv(os.path.join(folder, "countries.csv"))
df = df.where(pd.notnull(df), None)

batch = []
for _, row in df.iterrows():
    batch.append((row["id"], row["name"]))

execute_values(cursor, """
    INSERT INTO countries (id, name)
    VALUES %s
    ON CONFLICT (id) DO NOTHING
""", batch, page_size=500)

conn.commit()
print(f"  ✅ تم رفع {len(df)} صف\n")


# ══════════════════════════════════════════════════════════════
# governorates  (لازم يتحمل بعد countries)
# ══════════════════════════════════════════════════════════════
print("🏛️ بيرفع governorates...")

df = pd.read_csv(os.path.join(folder, "governorates.csv"))
df = df.where(pd.notnull(df), None)

batch = []
for _, row in df.iterrows():
    batch.append((row["id"], row["country_id"], row["name"]))

execute_values(cursor, """
    INSERT INTO governorates (id, country_id, name)
    VALUES %s
    ON CONFLICT (id) DO NOTHING
""", batch, page_size=500)

conn.commit()
print(f"  ✅ تم رفع {len(df)} صف\n")

# ── إغلاق الاتصال ────────────────────────────────────────────
cursor.close()
conn.close()
print("🎉 كل الداتا اتحملت على الداتابيز بنجاح!")
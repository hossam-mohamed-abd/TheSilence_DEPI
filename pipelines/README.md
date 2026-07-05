# Supabase Data Lake

## Purpose

Cloud storage used to store:

- Pharmacy uploaded files
- PIPLINE Proceccing
---

## Bucket Name

```text
medisearch-data-lake
```

---

## Folder Structure

```text
medisearch-data-lake/
│
├── pharmacy_uploads/
```

---

## Environment Variables

```env
SUPABASE_URL=https://qthxwtthzikwmmcnlxip.supabase.co
SUPABASE_KEY=sb_secret_GFuU_tmElpo_-yYJRgtyCQ_euYeapkL
```

---

## Python Connection

```python
from supabase import create_client

SUPABASE_URL = ""
SUPABASE_KEY = ""

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)
```

---

## Upload File

```python
with open("inventory.xlsx", "rb") as f:
    supabase.storage \
        .from_("medisearch-data-lake") \
        .upload(
            "pharmacy_uploads/inventory.xlsx",
            f
        )
```

---

## List Files

```python
files = (
    supabase.storage
    .from_("medisearch-data-lake")
    .list("pharmacy_uploads")
)
```

---

## Download File

```python
data = (
    supabase.storage
    .from_("medisearch-data-lake")
    .download(
        "pharmacy_uploads/inventory.xlsx"
    )
)
```

---

## Notes

- Use `service_role` only in Backend and Pipelines.
- Never expose keys in Frontend.
- Store secrets inside `.env`.

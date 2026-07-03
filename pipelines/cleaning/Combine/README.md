Here is a clean, concise `README.md` for your script:

```markdown
# Gardenia CSV Merger

A simple utility script to automatically find, load, and combine multiple CSV files from a specific folder into a single unified CSV file using Pandas.

## 🚀 Features
* **Automatic Discovery:** Automatically detects all `.csv` (case-insensitive) files inside the target directory.
* **Error Handling:** Gracefully skips corrupted or unreadable CSV files without crashing the execution loop.
* **Dynamic Paths:** Resolves relative folder paths automatically based on the script's absolute location.

## 📁 Directory Context
The script expects a subfolder named `Gardenia` in the same directory as the script itself:
```text
project/
│
├── combine_csvs_Gardenia.py
└── Gardenia/
    ├── file1.csv
    ├── file2.csv
    └── ...

```

## 💻 Setup & Usage

### 1. Install dependencies

```bash
pip install pandas

```

### 2. Run the script

```bash
python combine_csvs_Gardenia.py

```

## 📊 Output

Once execution finishes successfully, a single merged file will be generated in the parent directory:

* `combined_[[medications.csv`

```

```

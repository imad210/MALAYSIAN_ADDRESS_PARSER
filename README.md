![CI](https://github.com/imad210/MALAYSIAN_ADDRESS_PARSER/actions/workflows/ci.yml/badge.svg)
![PyPI](https://img.shields.io/pypi/v/malaysian-address-parser)
![License](https://img.shields.io/github/license/imad210/MALAYSIAN_ADDRESS_PARSER)

# Malaysian Address Parser

Deterministic, rule-based Malaysian address normalization engine built for messy real-world datasets.

This package extracts and standardizes Malaysian address strings into structured components:
```
ALAMAT1 | ALAMAT2 | ALAMAT3 | POSTCODE | STATE
```

Designed specifically for:

- Noisy Excel exports
- Local council datasets
- Mixed-format government records
- Inconsistent commas & whitespace
- Postcode false positives (LOT/PT/NO patterns)

---

# ✨ Features

- ✅ Rule-based (no ML dependency)
- ✅ Offline-capable
- ✅ Canonical Malaysian state mapping
- ✅ False-positive postcode protection
- ✅ MELAKA TENGAH special case handling
- ✅ CLI tool
- ✅ Excel batch processing
- ✅ Unit-tested (pytest)
- ✅ CI-enabled (GitHub Actions)

---

# 📦 Installation

## From PyPI (if published)
```bash
pip install malaysian-address-parser
```

## Local Development
```bash
pip install -e ".[dev,excel]"
```

Optional extras:

* `[excel]` → Excel processing (pandas + openpyxl)
* `[pdf]` → PDF extraction (camelot)
* `[dev]` → pytest + ruff

---

# 🚀 Usage

---

## 1️⃣ Parse Single Address (CLI)
```bash
malaysian-address-parser parse-one "Lot 123, Jalan Bunga, Taman Mawar, 70400 Seremban, Negeri Sembilan"
```

Pretty output:
```bash
malaysian-address-parser parse-one "..." --pretty
```

### Example Output
```json
{
  "alamat1": "LOT 123 JALAN BUNGA",
  "alamat2": "TAMAN MAWAR",
  "alamat3": "SEREMBAN",
  "poskod": "70400",
  "negeri": "NEGERI SEMBILAN DARUL KHUSUS"
}
```

---

## 2️⃣ Parse Excel File
```bash
malaysian-address-parser parse-excel input.xlsx --out output.xlsx
```

### Options

| Flag                 | Description                   |
| -------------------- | ----------------------------- |
| `--sheet`            | Sheet name or index           |
| `--col`              | Optional source column. If omitted, auto-detect all `ALAMAT_PENUH*` columns |
| `--out`              | Output file (.xlsx or .csv)   |
| `--limit`            | Limit rows (debug mode)       |
| `--no-keep-original` | Output only parsed fields     |

Example:
```bash
malaysian-address-parser parse-excel data/input.xlsx --out results/parsed.xlsx
```

Process only one specific source column:
```bash
malaysian-address-parser parse-excel data/input.xlsx --col ALAMAT_PENUH_ASET --out results/parsed.xlsx
```

Supports:

* Relative paths
* Absolute paths
* Auto-creates output directory if missing

### Auto-mapped Excel output

If your sheet contains:
```text
ALAMAT_PENUH_PEMILIK
ALAMAT_PENUH_ASET
```

the parser will automatically write into:
```text
ALAMAT1_PEMILIK | ALAMAT2_PEMILIK | ALAMAT3_PEMILIK | POSKOD_PEMILIK | NEGERI_PEMILIK
ALAMAT1_ASET    | ALAMAT2_ASET    | ALAMAT3_ASET    | POSKOD_ASET    | NEGERI_ASET
```

Existing target columns are replaced and reinserted next to the source
column, so the sheet layout stays aligned with the original dataset.

Field rules:

* **ALAMAT1** -> unit / blok / lot / jalan (`NO`, `UNIT`, `BLOK`, `JALAN`, `JLN`, `LORONG`, `PERSIARAN`)
* **ALAMAT2** -> taman / kampung / flat / kondo / apartment style area
* **ALAMAT3** -> selebihnya locality text sahaja
* **POSKOD** -> postcode sahaja
* **NEGERI** -> canonical state sahaja

---

# 🧠 Python API Usage
```python
from malaysian_address_parser import classify_address_v2

address = "Lot 123, Jalan Bunga, Taman Mawar, 70400 Seremban, Negeri Sembilan"

a1, a2, a3, poskod, negeri = classify_address_v2(address)

print(a1)
print(a2)
print(a3)
print(poskod)
print(negeri)
```

---

# 📂 Project Structure
```
.
├── src/
│   └── malaysian_address_parser/
│       ├── classifier.py
│       ├── alamat_splitter.py
│       ├── postcode_state_extractor.py
│       ├── pre_cleaner.py
│       ├── normalizer.py
│       ├── cli.py
│       └── excel_runner.py
│
├── tests/
│
├── .github/workflows/ci.yml
├── pyproject.toml
└── README.md
```

---

# 🔍 Core Logic Highlights

## Prefix Splitting

Splits prefix into:

* **ALAMAT1 (A1)** → Unit + Street
* **ALAMAT2 (A2)** → Area (Taman, Kampung, PPR, etc.)

Uses keyword-based heuristics instead of naive comma splitting.

---

## Postcode Detection

* Detects valid 5-digit Malaysian postcodes
* Ignores false positives like:
```
LOT 54321
PT 12345
```

Scoring system prefers postcodes appearing toward the end of address.

---

## State Canonicalization

Recognizes all Malaysian states including ceremonial names:

* JOHOR DARUL TAKZIM
* PERAK DARUL RIDZUAN
* SELANGOR DARUL EHSAN
* etc.

All states normalized into canonical format.

---

## Special Case Handling

Protected case:
```
MELAKA TENGAH
```

Prevents accidental stripping of "MELAKA" during state extraction.

---

# 🧪 Testing

Run tests locally:
```bash
pytest -q
```

CI runs tests across:

* Python 3.10
* Python 3.11
* Python 3.12
* Python 3.13

---

# ⚠ Known Limitations

* Extremely ambiguous rural addresses may require manual review
* No postcode ↔ state validation yet
* No gazette-level mukim verification
* Fully rule-based (no ML fallback)

---

# 🔮 Roadmap

* Postcode ↔ State validation layer
* Mukim-level canonical validation
* Performance benchmarking (rows/sec)
* Parallel Excel processing
* Docker packaging
* Web interface wrapper

---

# 🎯 Intended Use Cases

* Local authority datasets
* Asset registers
* CRM normalization
* Data migration projects
* License databases
* Cukai taksiran records
* Address standardization pipelines

---

# 📜 License

MIT

---

# Maintainer

Imaduddin  
Built for real Malaysian address data

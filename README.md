# MALAYSIAN_ADDRESS_PARSER

A modular Python tool for extracting, cleaning, and normalizing Malaysian addresses.

This system is specifically designed to handle common Malaysian address formats such as:

* Lot / PT numbers
* Taman
* Kampung
* Seksyen
* Bandar / Mukim
* Mixed-format Excel exports

The classifier splits raw address strings into standardized components:

```
A1 | A2 | A3 | POSTCODE | STATE
```

---

# 📂 Project Structure

```
MALAYSIAN_ADDRESS_PARSER/
│
├── data/                         # Input & output files (CSV / Excel)
│
├── scripts/
│   ├── classifier.py             # Main entry point for classification logic
│   ├── alamat_splitter.py        # Splits address prefix into A1 (Unit/Street) & A2 (Area)
│   ├── postcode_state_extractor.py # Extracts postcode & Malaysian state
│   ├── pre_cleaner.py            # Text standardization & whitespace cleanup
│   ├── normalizer.py             # Final formatting and output cleanup
│   ├── extract_pdf.py            # Extracts tabular data from PDF (MPKulai dataset use-case)
│   ├── main_driver_cukai.py      # Batch processor for tax (Cukai) files
│   └── main_driver_penjaja.py    # Batch processor for hawker/license files
│
├── .gitignore
└── README.md
```

---

# 🚀 Getting Started

## ✅ Prerequisites

* Python 3.10+
* pandas
* camelot (for PDF extraction)
* openpyxl (for Excel processing)

---

## 📦 Installation

To install these dependencies, run the following command in your terminal:

```bash
pip install -r requirements.txt
```

or 

```bash
pip install pandas camelot-py[cv] openpyxl
```

If using Camelot for PDF extraction, ensure:

* Ghostscript is installed on your system
* OpenCV dependencies are available

---

# 🛠 Usage

---

## 1️⃣ Extracting Data from PDF

If your raw dataset is in PDF format (e.g., MPKulai license list), use:

```bash
python scripts/extract_pdf.py
```

This script uses Camelot to extract tabular data into structured CSV/Excel format before classification.

---

## 2️⃣ Running the Address Classifier (Single Address)

The system classifies addresses into:

| Component        | Description                          |
| ---------------- | ------------------------------------ |
| **ALAMAT1 (A1)** | Unit, Lot, PT, Street name           |
| **ALAMAT2 (A2)** | Housing Area (Taman), Kampung, etc.  |
| **ALAMAT3 (A3)** | City / Sub-district (Bandar / Mukim) |
| **POSTCODE**     | 5-digit Malaysian postcode           |
| **STATE**        | Full canonical state name            |

### Example Implementation

```python
from scripts.classifier import classify_address_v2

address = "Lot 123, Jalan Bunga, Taman Mawar, 70400 Seremban, Negeri Sembilan"

a1, a2, a3, poskod, negeri = classify_address_v2(address)

print(f"Street: {a1}")
print(f"Area: {a2}")
print(f"City: {a3}")
print(f"Postcode: {poskod}")
print(f"State: {negeri}")
```

### Expected Output

```
Street: LOT 123 JALAN BUNGA
Area: TAMAN MAWAR
City: SEREMBAN
Postcode: 70400
State: NEGERI SEMBILAN
```

---

## 3️⃣ Batch Normalization (Excel Files)

To process entire datasets:

### For Assessment / Tax Files:

```bash
python scripts/main_driver_cukai.py
```

### For Hawker / Business License Files:

```bash
python scripts/main_driver_penjaja.py
```

Update the `input_xlsx` path inside:

```python
if __name__ == "__main__":
```

Block within each driver script.

---

# 🧠 Core Logic Highlights

---

## 🔹 Prefix Splitting Logic

Implemented inside:

```
alamat_splitter.py
```

Uses:

* `AREA_KEYWORDS` → Taman, Kampung, PPR, etc.
* `UNIT_KEYWORDS` → Lot, PT, No, HSD, GRN, etc.

This enables intelligent splitting between:

* A1 → Unit + Street
* A2 → Residential Area

Instead of relying purely on commas.

---

## 🔹 Postcode Protection Logic

Implemented inside:

```
postcode_state_extractor.py
```

The extractor:

* Identifies valid 5-digit Malaysian postcodes
* Ignores false positives such as:

```
PT 12345
LOT 54321
```

Prevents Lot numbers from being misclassified as postcodes.

---

## 🔹 State Extraction

Recognizes all Malaysian states in canonical format, including ceremonial titles such as:

* SELANGOR DARUL EHSAN
* PERAK DARUL RIDZUAN
* JOHOR DARUL TAKZIM
* KEDAH DARUL AMAN

State names are standardized before final output.

---

## 🔹 Special Case Protection

Includes protection for:

```
MELAKA TENGAH
```

Prevents the state name "Melaka" from being incorrectly stripped during city extraction.

This avoids truncation errors such as:

```
Incorrect → TENGAH
Correct   → MELAKA TENGAH
```

---

## 🔹 Pre-cleaning & Normalization

Handled by:

* `pre_cleaner.py`
* `normalizer.py`

Features include:

* Removing newlines
* Collapsing repeated commas
* Standardizing whitespace
* Converting output to uppercase
* Final trimming and formatting

---

# 📊 Output Format Summary

| Field    | Meaning              | Example             |
| -------- | -------------------- | ------------------- |
| A1       | Unit + Street        | LOT 123 JALAN BUNGA |
| A2       | Residential Area     | TAMAN MAWAR         |
| A3       | City / Mukim         | SEREMBAN            |
| POSTCODE | 5-digit code         | 70400               |
| STATE    | Canonical State Name | NEGERI SEMBILAN     |

---

# 🎯 Design Philosophy

This classifier is:

* Rule-based (not ML-dependent)
* Deterministic
* Offline-capable
* Optimized for Malaysian address structures
* Designed for messy real-world government datasets
* Suitable for large Excel files (100k+ rows)

---

# 🏢 Intended Use Cases

* PBT License Cleaning
* Local Council Databases
* Cukai Taksiran Records
* Penjaja License Records
* Asset Registers
* CRM Normalization
* Data Migration Projects

---

# 🔧 Customization

If address splits are incorrect:

### Update area detection:

Modify:

```
AREA_KEYWORDS
```

Inside:

```
alamat_splitter.py
```

---

### Adjust postcode detection logic:

Modify scoring rules in:

```
postcode_state_extractor.py
```

---

# ⚠️ Known Limitations

* Extremely ambiguous rural addresses may require manual review.
* Mukim-level validation is not yet cross-checked against official gazette lists.
* Does not currently validate postcode-to-state consistency.

---

# 🔮 Future Enhancements

* Mukim validation layer
* Postcode ↔ State cross-verification
* CLI wrapper tool
* Docker packaging
* Web interface
* Logging module for audit tracking

---

# 🤝 Contribution

Pull requests are welcome for:

* Additional edge case handling
* Improved splitting heuristics
* Performance optimization
* Enhanced state/postcode validation

---

# 📜 License

MIT

---

# 📌 Maintainer Notes

This project was designed specifically for Malaysian local authority datasets and real-world Excel exports where:

* Commas are inconsistent
* Postcodes are misplaced
* State titles are duplicated
* Lot numbers resemble postcodes

The logic prioritizes Malaysian addressing behavior over generic international formatting.

---

**MALAYSIAN_ADDRESS_PARSER**
Structured Malaysian Address Normalization — Built for Real Data.

import camelot
import pandas as pd
from pathlib import Path

# ===== CONFIG =====
PDF_PATH = Path("Senarai Pelesen Di MPKulai Tahun 2025.pdf")
OUTPUT_CSV = Path("mpkulai_lesen_2025_raw.csv")
OUTPUT_XLSX = Path("mpkulai_lesen_2025_raw.xlsx")

# Pages: kalau nak semua, guna "1-end" atau "1-518"
PAGES = "1-518"   # boleh tukar "1-10" dulu untuk test laju


def main():
    if not PDF_PATH.exists():
        raise FileNotFoundError(f"PDF tak jumpa: {PDF_PATH.resolve()}")

    print(f"📄 Baca PDF: {PDF_PATH}")
    print(f"   Pages: {PAGES}")
    # flavor=" ustream" sesuaintuk table tanpa garisan yang jelas
    tables = camelot.read_pdf(
        str(PDF_PATH),
        pages=PAGES,
        flavor="stream",
        strip_text="\n",   # buang newline dalam cell
    )

    print(f"✅ Jumlah table dikesan oleh Camelot: {tables.n}")

    if tables.n == 0:
        print("❌ Tiada table dikesan. Cuba:")
        print("   - Pastikan PDF betul")
        print("   - Cuba flavor='lattice'")
        return

    # ===== Gabungkan semua table ke satu DataFrame =====
    dfs = []
    for i, tbl in enumerate(tables):
        df = tbl.df.copy()
        df["__source_table__"] = i  # jejak datang dari table mana (optional)
        dfs.append(df)

    full_df = pd.concat(dfs, ignore_index=True)
    print(f"🔢 Bentuk DataFrame gabungan: {full_df.shape}")

    # ===== Optional: buang header berulang (baris yang mengandungi 'BIL NO. AKAUN') =====
    # Dari PDF, header dia ada text 'BIL NO. AKAUN', 'NAMA PELANGGAN' dll.
    # Kita detect dan buang row yang ada string 'BIL NO. AKAUN' dalam mana-mana kolum.
    mask_header = full_df.apply(lambda r: r.astype(str).str.contains("BIL NO. AKAUN").any(), axis=1)
    num_header_rows = mask_header.sum()
    if num_header_rows > 0:
        print(f"🧹 Buang {num_header_rows} baris header berulang.")
        full_df = full_df.loc[~mask_header].reset_index(drop=True)

    # ===== Save ke CSV & Excel =====
    full_df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
    try:
        full_df.to_excel(OUTPUT_XLSX, index=False)
    except Exception as e:
        print(f"⚠️ Tak dapat tulis Excel: {e}")

    print(f"💾 Siap simpan ke: {OUTPUT_CSV}")
    print(f"💾 (Jika berjaya) Excel: {OUTPUT_XLSX}")


if __name__ == "__main__":
    main()

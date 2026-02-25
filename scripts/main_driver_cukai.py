# main_driver_johor_excel.py
import pandas as pd
from classifier import classify_address_v2


def _normalize_one_side(
    df: pd.DataFrame,
    sumber_col: str,
    suffix: str,
):
    """
    sumber_col : nama column alamat penuh (cth: 'ALAMAT_PENUH_PEMILIK' / 'ALAMAT_PENUH_ASET')
    suffix     : 'PEMILIK' atau 'ASET'

    Akan isi/overwrite:
        ALAMAT1_{suffix}
        ALAMAT2_{suffix}
        ALAMAT3_{suffix}
        POSKOD_{suffix}
        NEGERI_{suffix}
    """

    if sumber_col not in df.columns:
        raise ValueError(f"Column '{sumber_col}' not found in input file.")

    a1_col = f"ALAMAT1_{suffix}"
    a2_col = f"ALAMAT2_{suffix}"
    a3_col = f"ALAMAT3_{suffix}"
    poskod_col = f"POSKOD_{suffix}"
    negeri_col = f"NEGERI_{suffix}"

    target_cols = [a1_col, a2_col, a3_col, poskod_col, negeri_col]

    # Pastikan column wujud & bertype string
    for col in target_cols:
        if col not in df.columns:
            df[col] = ""
        df[col] = df[col].astype("string")

    total = len(df)
    print(f"  [{suffix}] Normalizing {total} rows based on '{sumber_col}'")

    for idx, full_addr in df[sumber_col].items():
        if pd.isna(full_addr):
            full_addr = ""
        else:
            full_addr = str(full_addr)

        a1, a2, a3, poskod, negeri = classify_address_v2(full_addr)

        df.at[idx, a1_col] = a1
        df.at[idx, a2_col] = a2
        df.at[idx, a3_col] = a3
        df.at[idx, poskod_col] = poskod
        df.at[idx, negeri_col] = negeri

        if (idx + 1) % 50000 == 0:
            print(f"    [{suffix}] processed {idx + 1}/{total} rows...")

    # POSKOD as string (preserve 0 depan kalau ada)
    df[poskod_col] = df[poskod_col].astype("string")


def normalize_johor_from_excel(
    input_xlsx: str,
    output_csv_path: str,
    output_excel_path: str,
):
    """
    Baca Excel COMBINE_JOHOR_CUKAI.xlsx dan normalize:
      - ALAMAT_PENUH_PEMILIK -> *_PEMILIK
      - ALAMAT_PENUH_ASET    -> *_ASET

    DAN:
      - BANDAR_PEMILIK dikosongkan
      - BANDAR_ASET dikosongkan
    """

    print(f"[normalize_johor_from_excel] Reading Excel: {input_xlsx}")

    # Semua column sebagai string (elak dtype clash)
    df = pd.read_excel(input_xlsx, dtype=str, engine="openpyxl")

    # === Normalize alamat PEMILIK ===
    if "ALAMAT_PENUH_PEMILIK" in df.columns:
        _normalize_one_side(df, "ALAMAT_PENUH_PEMILIK", "PEMILIK")
    else:
        print("  WARNING: 'ALAMAT_PENUH_PEMILIK' not found - skipping PEMILIK normalization")

    # === Normalize alamat ASET ===
    if "ALAMAT_PENUH_ASET" in df.columns:
        _normalize_one_side(df, "ALAMAT_PENUH_ASET", "ASET")
    else:
        print("  WARNING: 'ALAMAT_PENUH_ASET' not found - skipping ASET normalization")

    # === Kosongkan BANDAR_PEMILIK & BANDAR_ASET ===
    if "BANDAR_PEMILIK" in df.columns:
        df["BANDAR_PEMILIK"] = ""
        df["BANDAR_PEMILIK"] = df["BANDAR_PEMILIK"].astype("string")
    else:
        # Kalau column tak wujud dan kau nak create pun boleh:
        df["BANDAR_PEMILIK"] = ""
        df["BANDAR_PEMILIK"] = df["BANDAR_PEMILIK"].astype("string")

    if "BANDAR_ASET" in df.columns:
        df["BANDAR_ASET"] = ""
        df["BANDAR_ASET"] = df["BANDAR_ASET"].astype("string")
    else:
        df["BANDAR_ASET"] = ""
        df["BANDAR_ASET"] = df["BANDAR_ASET"].astype("string")

    # Save to CSV
    print(f"[normalize_johor_from_excel] Saving CSV: {output_csv_path}")
    df.to_csv(output_csv_path, index=False)

    # Save to Excel
    print(f"[normalize_johor_from_excel] Saving Excel: {output_excel_path}")
    df.to_excel(output_excel_path, index=False)

    print("[normalize_johor_from_excel] Done.")


if __name__ == "__main__":
    # Tukar path ikut lokasi sebenar file Johor kau
    input_xlsx = r"C:\Users\monqichi\ML_projects\alamat_n9_classifier\selangor\pbt_pemilikanaset_huluselangor.xlsx"

    output_csv = r"C:\Users\monqichi\ML_projects\alamat_n9_classifier\selangor\pbt_pemilikanaset_huluselangor_normalized.csv"
    output_xlsx = r"C:\Users\monqichi\ML_projects\alamat_n9_classifier\selangor\pbt_pemilikanaset_huluselangor_normalized.xlsx"

    normalize_johor_from_excel(input_xlsx, output_csv, output_xlsx)

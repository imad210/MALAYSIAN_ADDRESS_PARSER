from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Optional, Union

LOG = logging.getLogger("malaysian_address_parser.excel")


def parse_excel_file(
    input_path: Path,
    sheet: Union[str, int] = 0,
    address_col: str = "address",
    out_path: Path = Path("parsed.xlsx"),
    limit: Optional[int] = None,
    keep_original: bool = True,
) -> None:
    """
    Read Excel -> parse addresses -> write Excel/CSV.

    Requires: pandas + openpyxl (install extras: pip install -e ".[excel]")
    """
    try:
        import pandas as pd
    except Exception as e:  # pragma: no cover
        raise RuntimeError(
            "Missing optional deps for Excel. Install with: pip install -e \".[excel]\""
        ) from e

    from .classifier import classify_address_v2

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    LOG.info("Reading: %s (sheet=%s)", input_path, sheet)
    df = pd.read_excel(input_path, sheet_name=sheet, dtype=str, engine="openpyxl")

    if address_col not in df.columns:
        raise ValueError(
            f"Column '{address_col}' not found. Available columns: {list(df.columns)}"
        )

    if limit is not None:
        df = df.head(limit).copy()

    def safe_parse(x: Any):
        if x is None:
            return ("", "", "", "", "")
        s = str(x).strip()
        if not s:
            return ("", "", "", "", "")
        return classify_address_v2(s)

    parsed = df[address_col].apply(safe_parse)

    out_df = df.copy() if keep_original else df[[address_col]].copy()

    out_df["alamat1"] = parsed.apply(lambda t: t[0])
    out_df["alamat2"] = parsed.apply(lambda t: t[1])
    out_df["alamat3"] = parsed.apply(lambda t: t[2])
    out_df["poskod"] = parsed.apply(lambda t: t[3])
    out_df["negeri"] = parsed.apply(lambda t: t[4])

    # Ensure output directory exists
    out_path.parent.mkdir(parents=True, exist_ok=True)

    out_suffix = out_path.suffix.lower()
    if out_suffix == ".csv":
        out_df.to_csv(out_path, index=False)
    elif out_suffix in [".xlsx", ".xlsm"]:
        out_df.to_excel(out_path, index=False)
    else:
        raise ValueError("Output must be .xlsx/.xlsm or .csv")
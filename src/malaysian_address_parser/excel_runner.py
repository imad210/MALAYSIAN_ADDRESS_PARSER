from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Optional, Sequence, Union

LOG = logging.getLogger("malaysian_address_parser.excel")

DEFAULT_OUTPUT_COLUMNS = ("alamat1", "alamat2", "alamat3", "poskod", "negeri")


def _derive_output_columns(address_col: str) -> tuple[str, str, str, str, str]:
    upper_col = address_col.upper()
    if upper_col.startswith("ALAMAT_PENUH"):
        suffix = address_col[len("ALAMAT_PENUH") :]
        return (
            f"ALAMAT1{suffix}",
            f"ALAMAT2{suffix}",
            f"ALAMAT3{suffix}",
            f"POSKOD{suffix}",
            f"NEGERI{suffix}",
        )
    return DEFAULT_OUTPUT_COLUMNS


def _detect_address_columns(columns: Sequence[str]) -> list[str]:
    detected = [column for column in columns if str(column).upper().startswith("ALAMAT_PENUH")]
    if detected:
        return detected

    for column in columns:
        if str(column).lower() == "address":
            return [column]

    return []


def _resolve_address_columns(
    available_columns: Sequence[str], address_col: Optional[str]
) -> list[str]:
    if address_col:
        if address_col not in available_columns:
            raise ValueError(
                f"Column '{address_col}' not found. Available columns: {list(available_columns)}"
            )
        return [address_col]

    detected_columns = _detect_address_columns(available_columns)
    if detected_columns:
        return detected_columns

    raise ValueError(
        "No ALAMAT_PENUH* column found. "
        f"Available columns: {list(available_columns)}"
    )


def _safe_parse_address(value: Any, classify_address_v2: Any) -> tuple[str, str, str, str, str]:
    if value is None:
        return ("", "", "", "", "")

    text = str(value).strip()
    if not text:
        return ("", "", "", "", "")

    return classify_address_v2(text)


def _replace_columns_next_to_source(out_df: Any, source_col: str, parsed_df: Any) -> Any:
    target_columns = list(parsed_df.columns)
    existing_targets = [column for column in target_columns if column in out_df.columns]
    if existing_targets:
        out_df = out_df.drop(columns=existing_targets)

    insert_at = out_df.columns.get_loc(source_col) + 1
    for offset, column in enumerate(target_columns):
        out_df.insert(insert_at + offset, column, parsed_df[column])
    return out_df


def parse_excel_file(
    input_path: Path,
    sheet: Union[str, int] = 0,
    address_col: Optional[str] = None,
    out_path: Path = Path("parsed.xlsx"),
    limit: Optional[int] = None,
    keep_original: bool = True,
) -> None:
    """
    Read Excel -> parse addresses -> write Excel/CSV.

    Behavior:
    - If `address_col` is provided, only that source column is processed.
    - If omitted, auto-detect all `ALAMAT_PENUH*` columns.
    - For `ALAMAT_PENUH_*`, outputs are written into matching
      `ALAMAT1_*`, `ALAMAT2_*`, `ALAMAT3_*`, `POSKOD_*`, `NEGERI_*` columns.
    - Existing target columns are replaced next to the source column.

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

    if limit is not None:
        df = df.head(limit).copy()

    address_columns = _resolve_address_columns(list(df.columns), address_col)
    LOG.info("Processing address columns: %s", ", ".join(address_columns))

    if keep_original:
        out_df = df.copy()
        for source_col in address_columns:
            output_columns = _derive_output_columns(source_col)
            LOG.info("Mapping %s -> %s", source_col, ", ".join(output_columns))
            parsed = df[source_col].apply(
                lambda value: _safe_parse_address(value, classify_address_v2)
            )
            parsed_df = pd.DataFrame(parsed.tolist(), columns=output_columns, index=df.index)
            out_df = _replace_columns_next_to_source(out_df, source_col, parsed_df)
    else:
        out_df = pd.DataFrame(index=df.index)
        for source_col in address_columns:
            output_columns = _derive_output_columns(source_col)
            LOG.info("Mapping %s -> %s", source_col, ", ".join(output_columns))
            parsed = df[source_col].apply(
                lambda value: _safe_parse_address(value, classify_address_v2)
            )
            out_df[source_col] = df[source_col]
            parsed_df = pd.DataFrame(parsed.tolist(), columns=output_columns, index=df.index)
            for column in parsed_df.columns:
                out_df[column] = parsed_df[column]

    # Ensure output directory exists
    out_path.parent.mkdir(parents=True, exist_ok=True)

    out_suffix = out_path.suffix.lower()
    if out_suffix == ".csv":
        out_df.to_csv(out_path, index=False)
    elif out_suffix in [".xlsx", ".xlsm"]:
        out_df.to_excel(out_path, index=False)
    else:
        raise ValueError("Output must be .xlsx/.xlsm or .csv")

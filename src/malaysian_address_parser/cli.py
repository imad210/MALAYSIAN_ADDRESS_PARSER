from __future__ import annotations

import argparse
import json
import logging
import os
from pathlib import Path
from typing import Any


LOG = logging.getLogger("malaysian_address_parser")


def _setup_logging(verbose: bool = False) -> None:
    level = os.environ.get("MALAYSIA_ADDR_LOG_LEVEL", "INFO").upper()
    if verbose:
        level = "DEBUG"
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="malaysian-address-parser")
    p.add_argument("-v", "--verbose", action="store_true", help="Enable debug logs")

    sub = p.add_subparsers(dest="cmd", required=True)

    one = sub.add_parser("parse-one", help="Parse a single address string")
    one.add_argument("text", help="Address text")
    one.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")

    excel = sub.add_parser("parse-excel", help="Parse an Excel file column")
    excel.add_argument("input", type=Path, help="Input .xlsx file")
    excel.add_argument("--sheet", default=0, help="Sheet name or index (default: 0)")
    excel.add_argument("--col", required=True, help="Column name containing address text")
    excel.add_argument("--out", type=Path, required=True, help="Output .xlsx/.xlsm or .csv")
    excel.add_argument("--limit", type=int, default=None, help="Limit rows (debugging)")
    excel.add_argument(
        "--keep-original",
        action="store_true",
        help="Keep original columns (default: True). Use --no-keep-original to output only parsed fields.",
    )
    excel.add_argument(
        "--no-keep-original",
        dest="keep_original",
        action="store_false",
        help="Output only parsed fields.",
    )
    excel.set_defaults(keep_original=True)

    return p


def _print_json(obj: Any, pretty: bool) -> None:
    if pretty:
        print(json.dumps(obj, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(obj, ensure_ascii=False))


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    _setup_logging(args.verbose)

    if args.cmd == "parse-one":
        from .classifier import classify_address_v2

        a1, a2, a3, poskod, negeri = classify_address_v2(args.text)
        payload = {
            "alamat1": a1,
            "alamat2": a2,
            "alamat3": a3,
            "poskod": poskod,
            "negeri": negeri,
        }
        _print_json(payload, args.pretty)
        return 0

    if args.cmd == "parse-excel":
        from .excel_runner import parse_excel_file

        parse_excel_file(
            input_path=args.input,
            sheet=args.sheet,
            address_col=args.col,
            out_path=args.out,
            limit=args.limit,
            keep_original=args.keep_original,
        )
        LOG.info("Done. Output written to: %s", args.out)
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
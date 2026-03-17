from __future__ import annotations

import re
from typing import Tuple

AREA_KEYWORDS = [
    "TAMAN",
    "KAMPUNG",
    "KG",
    "FELDA",
    "RUMAH RAKYAT",
    "SEKSYEN",
    "SEKSEN",
    "GUGUSAN",
    "APARTMENT",
    "APARTMEN",
    "PANGSAPURI",
    "DESA",
    "RESIDENSI",
    "PPR",
    "FLAT",
    "KONDO",
    "KONDOMINIUM",
    "CONDOMINIUM",
]

ROAD_KEYWORDS = [
    "JALAN",
    "JLN",
    "LORONG",
    "LRG",
    "PERSIARAN",
    "PSRN",
    "LEBUH",
    "LBH",
    "JALANRAYA",
]
UNIT_KEYWORDS = [
    "LOT",
    "PT",
    "NO",
    "BLOK",
    "BLK",
    "TINGKAT",
    "TKT",
    "UNIT",
    "PASAR",
    "GERAI",
    "KEDAI",
    "BATU",
    "KM",
]


def _compile_keyword_re(keywords: list[str]) -> re.Pattern[str]:
    parts = sorted((re.escape(keyword) for keyword in keywords), key=len, reverse=True)
    return re.compile(r"\b(?:" + "|".join(parts) + r")\b", re.IGNORECASE)


ROAD_RE = _compile_keyword_re(ROAD_KEYWORDS)
AREA_RE = _compile_keyword_re(AREA_KEYWORDS)
UNIT_RE = _compile_keyword_re(UNIT_KEYWORDS)
HAS_DIGIT_RE = re.compile(r"\d")


def _join_parts(parts: list[str]) -> str:
    return ", ".join(parts).strip(" ,")


def classify_prefix_token(token: str) -> str:
    if not token:
        return "other"

    token_upper = token.upper()

    if AREA_RE.search(token_upper):
        return "a2"
    if ROAD_RE.search(token_upper) or UNIT_RE.search(token_upper):
        return "a1"
    if HAS_DIGIT_RE.search(token_upper):
        return "a1"
    return "other"


def split_prefix_into_components(prefix: str) -> Tuple[str, str, str]:
    if not prefix:
        return "", "", ""

    tokens = [t.strip() for t in prefix.split(",") if t.strip()]
    a1_parts: list[str] = []
    a2_parts: list[str] = []
    other_parts: list[str] = []

    for tok in tokens:
        role = classify_prefix_token(tok)
        if role == "a1":
            a1_parts.append(tok)
        elif role == "a2":
            a2_parts.append(tok)
        else:
            other_parts.append(tok)

    return _join_parts(a1_parts), _join_parts(a2_parts), _join_parts(other_parts)


def split_prefix_into_a1_a2(prefix: str) -> Tuple[str, str]:
    """
    Split address prefix into:
    - A1: unit/road style tokens (LOT/PT/NO/JALAN/...)
    - A2: area style tokens (TAMAN/KG/PPR/...)
    """
    a1, a2, _ = split_prefix_into_components(prefix)
    return a1, a2

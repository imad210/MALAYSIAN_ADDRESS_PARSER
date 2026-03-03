from __future__ import annotations

import re
from typing import Tuple

AREA_KEYWORDS = [
    "TAMAN", "KAMPUNG", "KG", "FELDA", "RUMAH RAKYAT", "SEKSYEN", "SEKSEN",
    "GUGUSAN", "APARTMENT", "PANGSAPURI", "DESA", "RESIDENSI", "PPR", "FLAT",
]

UNIT_KEYWORDS = ["LOT", "PT", "NO", "BLOK", "BLK", "TINGKAT", "TKT", "UNIT", "PASAR", "GERAI", "KEDAI", "BATU", "KM"]
UNIT_RE = re.compile(r"\b(" + "|".join(UNIT_KEYWORDS) + r")\b", re.IGNORECASE)


def split_prefix_into_a1_a2(prefix: str) -> Tuple[str, str]:
    """
    Split address prefix into:
    - A1: unit/road style tokens (LOT/PT/NO/JALAN/...)
    - A2: area style tokens (TAMAN/KG/PPR/...)
    """
    if not prefix:
        return "", ""

    tokens = [t.strip() for t in prefix.split(",") if t.strip()]
    a1_parts: list[str] = []
    a2_parts: list[str] = []

    for tok in tokens:
        t_up = tok.upper()

        if "JALAN" in t_up or UNIT_RE.search(t_up):
            a1_parts.append(tok)
        elif any(kw in t_up for kw in AREA_KEYWORDS):
            a2_parts.append(tok)
        else:
            # fallback heuristic
            if len(tok) < 12:
                a1_parts.append(tok)
            else:
                a2_parts.append(tok)

    return ", ".join(a1_parts).strip(" ,"), ", ".join(a2_parts).strip(" ,")
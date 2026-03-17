from __future__ import annotations

from typing import Tuple

from .alamat_splitter import split_prefix_into_a1_a2, split_prefix_into_components
from .normalizer import normalize_component
from .postcode_state_extractor import (
    extract_alamat3,
    extract_postcode_idx,
    extract_state,
)
from .pre_cleaner import clean_text


def _split_state_from_tail(text: str) -> Tuple[str, str]:
    tokens = [token.strip() for token in text.split(",") if token.strip()]
    if not tokens:
        return "", ""

    last_token = tokens[-1]
    negeri = extract_state(last_token)
    if negeri:
        return ",".join(tokens[:-1]).strip(" ,"), negeri
    return text, ""


def classify_address_v2(full_text: str) -> Tuple[str, str, str, str, str]:
    """
    Deterministic classifier:
      input -> (alamat1, alamat2, alamat3, poskod, negeri)

    Notes:
    - Uses postcode detection + state detection heuristics
    - Extracts "alamat3" from segment after postcode (with "MELAKA TENGAH" protection)
    - Splits prefix into A1 (unit/jalan) and A2 (kawasan) using keyword heuristics
    """
    cleaned = clean_text(full_text)
    poskod, p_idx = extract_postcode_idx(cleaned)
    prefix_without_state, tail_state = _split_state_from_tail(cleaned)
    negeri = extract_state(cleaned) or tail_state

    a1 = a2 = a3_final = ""

    if p_idx is not None and poskod:
        a3_hujung = extract_alamat3(cleaned, poskod, p_idx)
        prefix = cleaned[:p_idx].strip(" ,")

        a1, a2 = split_prefix_into_a1_a2(prefix)

        # If postcode tail has no bandar/mukim token, use leftover prefix tokens that are neither road nor area.
        if not a3_hujung:
            a1, a2, a3_candidate = split_prefix_into_components(prefix)
            a3_final = a3_candidate
        else:
            a3_final = a3_hujung
    else:
        a1, a2, a3_final = split_prefix_into_components(prefix_without_state)

    # Final cleanup / formatting (consistent output)
    return (
        normalize_component(a1),
        normalize_component(a2),
        normalize_component(a3_final),
        normalize_component(poskod),
        normalize_component(negeri),
    )

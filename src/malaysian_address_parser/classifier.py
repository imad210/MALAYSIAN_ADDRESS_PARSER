from __future__ import annotations

from typing import Tuple

from .alamat_splitter import split_prefix_into_a1_a2
from .normalizer import normalize_component
from .postcode_state_extractor import extract_alamat3, extract_postcode_idx, extract_state
from .pre_cleaner import clean_text


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
    negeri = extract_state(cleaned)

    a1 = a2 = a3_final = ""

    if p_idx is not None and poskod:
        a3_hujung = extract_alamat3(cleaned, poskod, p_idx)
        prefix = cleaned[:p_idx].strip(" ,")

        a1, a2 = split_prefix_into_a1_a2(prefix)

        # If alamat3 extraction failed, try use "last token" as bandar/mukim (only if it's not unit/jalan)
        if not a3_hujung:
            prefix_tokens = [t.strip() for t in prefix.split(",") if t.strip()]
            if prefix_tokens:
                last_token = prefix_tokens[-1].strip()
                if not any(k in last_token.upper() for k in ["JALAN", "LOT", "PT", "NO"]):
                    a3_final = last_token
                    new_prefix = ",".join(prefix_tokens[:-1])
                    a1, a2 = split_prefix_into_a1_a2(new_prefix)
                else:
                    a3_final = ""
        else:
            a3_final = a3_hujung
    else:
        a1, a2 = split_prefix_into_a1_a2(cleaned)
        a3_final = ""

    # Final cleanup / formatting (consistent output)
    return (
        normalize_component(a1),
        normalize_component(a2),
        normalize_component(a3_final),
        normalize_component(poskod),
        normalize_component(negeri),
    )
# normalizer_v2.py

from typing import Optional

def normalize_alamat3(raw_seg: Optional[str]) -> str:
    """
    Currently we just strip extra commas/spaces.
    (We keep original casing & 'DARUL KHUSUS' etc.)
    """
    if not raw_seg:
        return ""
    return raw_seg.strip(" ,")

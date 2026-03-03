from __future__ import annotations

import re
from typing import Optional


_SPACE_RE = re.compile(r"\s{2,}")
_COMMA_RE = re.compile(r",\s*,+")


def normalize_component(val: Optional[str]) -> str:
    """
    Final formatting for output fields:
    - None -> ""
    - collapse whitespace
    - collapse repeated commas
    - strip commas/spaces
    - uppercase (consistent for analytics joins)
    """
    if not val:
        return ""
    s = str(val)
    s = s.replace("\n", " ").replace("\r", " ")
    s = _COMMA_RE.sub(", ", s)
    s = _SPACE_RE.sub(" ", s)
    s = s.strip(" ,")
    return s.upper()
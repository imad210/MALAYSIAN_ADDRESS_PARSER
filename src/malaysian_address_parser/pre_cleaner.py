from __future__ import annotations

import re
from typing import Any


_COMMA_RE = re.compile(r",\s*,+")
_SPACE_RE = re.compile(r"\s{2,}")


def clean_text(val: Any) -> str:
    """
    Basic cleanup:
    - ensure string
    - normalize newlines
    - collapse multiple commas / spaces
    - strip leading/trailing commas & spaces
    """
    if val is None:
        return ""
    s = str(val)

    s = s.replace("\n", " ").replace("\r", " ")
    s = _COMMA_RE.sub(", ", s)
    s = _SPACE_RE.sub(" ", s)
    s = s.strip(" ,")

    return s
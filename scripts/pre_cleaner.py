# pre_cleaner_v2.py
import re

def clean_text(val: str) -> str:
    """
    Basic cleanup:
    - ensure string
    - collapse multiple commas / spaces
    - strip leading/trailing commas & spaces
    """
    if val is None:
        return ""
    s = str(val)

    # Normalise whitespace-ish chars
    s = s.replace("\n", " ").replace("\r", " ")

    # Collapse repeated commas
    s = re.sub(r",\s*,+", ", ", s)

    # Collapse repeated spaces
    s = re.sub(r"\s{2,}", " ", s)

    # Strip leading/trailing commas + spaces
    s = s.strip(" ,")

    return s

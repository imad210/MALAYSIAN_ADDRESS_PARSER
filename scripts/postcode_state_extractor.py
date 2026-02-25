import re
from typing import Optional, Tuple

STATE_CANONICAL = {
    "JOHOR": "JOHOR DARUL TAKZIM",
    "JOHOR DARUL TAKZIM": "JOHOR DARUL TAKZIM",
    "KEDAH": "KEDAH DARUL AMAN",
    "KEDAH DARUL AMAN": "KEDAH DARUL AMAN",
    "KELANTAN": "KELANTAN DARUL NAIM",
    "KELANTAN DARUL NAIM": "KELANTAN DARUL NAIM",
    "MELAKA": "MELAKA",
    "MALACCA": "MELAKA",
    "NEGERI SEMBILAN": "NEGERI SEMBILAN DARUL KHUSUS",
    "NEGERI SEMBILAN DARUL KHUSUS": "NEGERI SEMBILAN DARUL KHUSUS",
    "PAHANG": "PAHANG DARUL MAKMUR",
    "PAHANG DARUL MAKMUR": "PAHANG DARUL MAKMUR",
    "PERAK": "PERAK DARUL RIDZUAN",
    "PERAK DARUL RIDZUAN": "PERAK DARUL RIDZUAN",
    "PERLIS": "PERLIS",
    "PERLIS INDERA KAYANGAN": "PERLIS",
    "PULAU PINANG": "PULAU PINANG",
    "PENANG": "PULAU PINANG",
    "SABAH": "SABAH",
    "SABAH NEGERI DI BAWAH BAYU": "SABAH",
    "SARAWAK": "SARAWAK",
    "SARAWAK NEGERI BERTUAH": "SARAWAK",
    "SELANGOR": "SELANGOR DARUL EHSAN",
    "SELANGOR DARUL EHSAN": "SELANGOR DARUL EHSAN",
    "TERENGGANU": "TERENGGANU",
    "TERENGGANU DARUL IMAN": "TERENGGANU",
    "KUALA LUMPUR": "KUALA LUMPUR",
    "KUALA LUMPUR WILAYAH PERSEKUTUAN (KUALA LUMPUR)": "KUALA LUMPUR",
    "WILAYAH PERSEKUTUAN KUALA LUMPUR": "KUALA LUMPUR",
    "PUTRAJAYA": "PUTRAJAYA",
    "PUTRAJAYA WILAYAH PERSEKUTUAN (PUTRAJAYA)": "PUTRAJAYA",
    "WILAYAH PERSEKUTUAN PUTRAJAYA": "PUTRAJAYA",
    "LABUAN": "LABUAN",
    "LABUAN WILAYAH PERSEKUTUAN (LABUAN)": "LABUAN",
    "WILAYAH PERSEKUTUAN LABUAN": "LABUAN",
}

# Regex untuk kesan 5 digit
_FIVE_DIGIT_RE = re.compile(r"\b(\d{5})\b")
_LOT_PREFIX_RE = re.compile(r"\b(LOT|PT|P\.T|NO|NO\.)\s*$", re.IGNORECASE)

# Regex untuk buang Negeri & Gelaran Negeri (Darul...)
# Kita guna word boundary \b supaya tak terpotong sebahagian daripada perkataan lain
NEGERI_EXTENDED_RE = re.compile(
    r"\b(PERAK|SELANGOR|JOHOR|KEDAH|KELANTAN|TERENGGANU|PAHANG|MELAKA|NEGERI SEMBILAN|PULAU PINANG|PERLIS|SABAH|SARAWAK|KUALA LUMPUR|PUTRAJAYA|DARUL\s?\w+)\b", 
    re.IGNORECASE
)

def extract_postcode_idx(text: str) -> Tuple[Optional[str], Optional[int]]:
    if not text: return None, None
    candidates = []
    for match in _FIVE_DIGIT_RE.finditer(text):
        code = match.group(1)
        start = match.start()
        before_text = text[max(0, start-15):start].strip()
        if _LOT_PREFIX_RE.search(before_text): continue
            
        score = 0
        if start > (len(text) * 0.4): score += 2
        after_text = text[start:].upper()
        for state in STATE_CANONICAL:
            if state in after_text:
                score += 10
                break
        candidates.append((score, start, code))
    
    if not candidates: return None, None
    candidates.sort(key=lambda x: x[0], reverse=True)
    return candidates[0][2], candidates[0][1]

def extract_state(text: str) -> Optional[str]:
    if not text: return None
    t = text.upper()
    for s in STATE_CANONICAL:
        if s in t: return STATE_CANONICAL[s]
    return None

def extract_alamat3(text: str, postcode: str, postcode_idx: int) -> str:
    if not text or postcode_idx is None: return ""
    
    # 1. Ambil baki alamat SELEPAS poskod
    seg = text[postcode_idx + 5:].strip(" ,")
    
    # 2. PROTECT "MELAKA TENGAH": Tukar sementara ke placeholder unik
    # supaya sistem pembersihan tak nampak perkataan "MELAKA" tu
    seg = re.sub(r"\bMELAKA TENGAH\b", "##MT##", seg, flags=re.IGNORECASE)
    
    # 3. Buang Negeri & Gelaran (Darul...)
    seg = NEGERI_EXTENDED_RE.sub("", seg).strip(" ,")
    
    # 4. RESTORE "MELAKA TENGAH"
    seg = seg.replace("##MT##", "MELAKA TENGAH")
    seg = seg.replace("##mt##", "MELAKA TENGAH")
    
    # 5. Final cleaning
    seg = re.sub(r"[-/,]+$", "", seg).strip(" ,")
    
    return seg
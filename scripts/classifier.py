from pre_cleaner import clean_text
from postcode_state_extractor import (
    extract_postcode_idx,
    extract_state,
    extract_alamat3,
)
from normalizer import normalize_alamat3
from alamat_splitter import split_prefix_into_a1_a2

def classify_address_v2(full_text: str):
    cleaned = clean_text(full_text)
    
    poskod, p_idx = extract_postcode_idx(cleaned)
    negeri = extract_state(cleaned)

    if p_idx is not None:
        # Alamat 3 sekarang dah ada protection untuk Melaka Tengah
        a3_hujung = extract_alamat3(cleaned, poskod, p_idx)
        prefix = cleaned[:p_idx].strip(" ,")
        
        a1, a2 = split_prefix_into_a1_a2(prefix)
        
        if not a3_hujung:
            prefix_tokens = prefix.split(",")
            last_token = prefix_tokens[-1].strip()
            
            # Logic check bandar
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

    return (
        a1 or "",
        a2 or "",
        a3_final or "",
        poskod or "",
        negeri or "",
    )
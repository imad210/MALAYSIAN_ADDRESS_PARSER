from malaysian_address_parser.postcode_state_extractor import (
    extract_alamat3,
    extract_postcode_idx,
    extract_state,
)


def test_extract_postcode_idx_basic():
    text = "LOT 12, JALAN BUNGA, 16150 KOTA BHARU KELANTAN"
    code, idx = extract_postcode_idx(text)
    assert code == "16150"
    assert idx is not None


def test_extract_postcode_idx_ignores_lot_prefix_false_positive():
    # should ignore when 5 digits appears right after LOT/PT/NO prefix (common noisy cases)
    text = "LOT 16150, KOTA BHARU, KELANTAN"
    code, idx = extract_postcode_idx(text)
    # In this case, it's ambiguous; our heuristic should likely ignore it → return None
    assert code is None
    assert idx is None


def test_extract_state_canonical():
    text = "KOTA BHARU, KELANTAN"
    state = extract_state(text)
    assert state == "KELANTAN DARUL NAIM"


def test_extract_alamat3_basic_removes_state_tail():
    text = "LOT 12, JALAN BUNGA, 16150 KOTA BHARU KELANTAN"
    code, idx = extract_postcode_idx(text)
    assert code == "16150"
    assert idx is not None
    a3 = extract_alamat3(text, code, idx)
    # expected to keep bandar-ish tail but remove state tokens
    assert "KELANTAN" not in a3.upper()
    assert "KOTA BHARU" in a3.upper()


def test_extract_alamat3_protects_melaka_tengah():
    text = "NO 1, JALAN ABC, 75450 MELAKA TENGAH MELAKA"
    code, idx = extract_postcode_idx(text)
    assert code == "75450"
    assert idx is not None
    a3 = extract_alamat3(text, code, idx)
    assert "MELAKA TENGAH" in a3.upper()
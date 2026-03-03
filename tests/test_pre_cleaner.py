from malaysian_address_parser.pre_cleaner import clean_text


def test_clean_text_none():
    assert clean_text(None) == ""


def test_clean_text_basic():
    s = "  LOT 12,,  KG ABC \n 16150  "
    out = clean_text(s)
    assert out == "LOT 12, KG ABC 16150"


def test_clean_text_collapse_spaces():
    s = "NO  12     JALAN   BUNGA"
    out = clean_text(s)
    assert out == "NO 12 JALAN BUNGA"
from malaysian_address_parser.classifier import classify_address_v2


def test_classify_with_postcode_and_state():
    text = "Lot 12, Jalan Bunga, Taman Mawar, 70400 Seremban, Negeri Sembilan"
    a1, a2, a3, poskod, negeri = classify_address_v2(text)

    assert poskod == "70400"
    assert "NEGERI SEMBILAN" in negeri  # canonical may include DARUL KHUSUS
    assert "JALAN" in a1
    assert "TAMAN" in a2
    # alamat3 should be something like SEREMBAN
    assert a3 != ""


def test_classify_without_postcode():
    text = "PT 1234, KG ABC, PASIR MAS, KELANTAN"
    a1, a2, a3, poskod, negeri = classify_address_v2(text)

    assert poskod == ""
    assert negeri == "KELANTAN DARUL NAIM"
    assert a1 != "" or a2 != ""


def test_classify_melaka_tengah_case():
    text = "NO 1, JALAN ABC, 75450 MELAKA TENGAH MELAKA"
    a1, a2, a3, poskod, negeri = classify_address_v2(text)

    assert poskod == "75450"
    # extractor protects MELAKA TENGAH from being broken
    assert "MELAKA TENGAH" in a3


def test_output_is_uppercase_and_trimmed():
    text = "  Lot 12,, Jalan Bunga ,  16150 Kota Bharu Kelantan  "
    a1, a2, a3, poskod, negeri = classify_address_v2(text)

    assert a1 == a1.strip(" ,")
    assert poskod == "16150"
    assert negeri == "KELANTAN DARUL NAIM"
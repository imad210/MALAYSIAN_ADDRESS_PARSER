from malaysian_address_parser.alamat_splitter import split_prefix_into_a1_a2


def test_split_prefix_simple():
    prefix = "LOT 12, JALAN BUNGA, TAMAN MAWAR"
    a1, a2 = split_prefix_into_a1_a2(prefix)
    assert "LOT 12" in a1.upper()
    assert "JALAN" in a1.upper()
    assert "TAMAN" in a2.upper()


def test_split_prefix_empty():
    a1, a2 = split_prefix_into_a1_a2("")
    assert a1 == ""
    assert a2 == ""
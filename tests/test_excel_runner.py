import pytest


def test_parse_excel_file_roundtrip(tmp_path):
    pd = pytest.importorskip("pandas")

    from malaysian_address_parser.excel_runner import parse_excel_file

    inp = tmp_path / "input.xlsx"
    out = tmp_path / "out.xlsx"

    df = pd.DataFrame(
        {
            "address": [
                "Lot 12, Jalan Bunga, Taman Mawar, 70400 Seremban, Negeri Sembilan",
                "NO 1, JALAN ABC, 75450 MELAKA TENGAH MELAKA",
                "",
                None,
            ]
        }
    )
    df.to_excel(inp, index=False)

    parse_excel_file(
        input_path=inp,
        sheet=0,
        address_col="address",
        out_path=out,
        keep_original=True,
    )

    assert out.exists()

    out_df = pd.read_excel(out)
    # basic columns existence
    for c in ["alamat1", "alamat2", "alamat3", "poskod", "negeri"]:
        assert c in out_df.columns

    assert str(out_df.loc[0, "poskod"]) == "70400"


def test_parse_excel_file_autodetects_alamat_penuh_suffix_columns(tmp_path):
    pd = pytest.importorskip("pandas")

    from malaysian_address_parser.excel_runner import parse_excel_file

    inp = tmp_path / "input.xlsx"
    out = tmp_path / "out.xlsx"

    df = pd.DataFrame(
        {
            "NO_KP": ["1"],
            "ALAMAT_PENUH_ASET": ["62 JLN MELUR, TAMAN MELUR, 68000, AMPANG"],
            "ALAMAT1_ASET": [""],
            "ALAMAT2_ASET": [""],
            "ALAMAT3_ASET": [""],
            "POSKOD_ASET": [""],
            "NEGERI_ASET": [""],
            "ALAMAT_PENUH_PEMILIK": ["PT 1234, KG ABC, PASIR MAS, KELANTAN"],
            "ALAMAT1_PEMILIK": [""],
            "ALAMAT2_PEMILIK": [""],
            "ALAMAT3_PEMILIK": [""],
            "POSKOD_PEMILIK": [""],
            "NEGERI_PEMILIK": [""],
        }
    )
    df.to_excel(inp, index=False)

    parse_excel_file(input_path=inp, sheet=0, out_path=out, keep_original=True)

    out_df = pd.read_excel(out, dtype=str).fillna("")

    assert out_df.loc[0, "ALAMAT1_ASET"] == "62 JLN MELUR"
    assert out_df.loc[0, "ALAMAT2_ASET"] == "TAMAN MELUR"
    assert out_df.loc[0, "ALAMAT3_ASET"] == "AMPANG"
    assert out_df.loc[0, "POSKOD_ASET"] == "68000"
    assert out_df.loc[0, "NEGERI_ASET"] == ""
    assert out_df.loc[0, "ALAMAT1_PEMILIK"] == "PT 1234"
    assert out_df.loc[0, "ALAMAT2_PEMILIK"] == "KG ABC"
    assert out_df.loc[0, "ALAMAT3_PEMILIK"] == "PASIR MAS"
    assert out_df.loc[0, "POSKOD_PEMILIK"] == ""
    assert out_df.loc[0, "NEGERI_PEMILIK"] == "KELANTAN DARUL NAIM"

    aset_col_pos = list(out_df.columns).index("ALAMAT_PENUH_ASET")
    assert out_df.columns[aset_col_pos + 1 : aset_col_pos + 6].tolist() == [
        "ALAMAT1_ASET",
        "ALAMAT2_ASET",
        "ALAMAT3_ASET",
        "POSKOD_ASET",
        "NEGERI_ASET",
    ]

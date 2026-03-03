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
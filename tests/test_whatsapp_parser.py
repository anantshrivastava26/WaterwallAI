from ingestion.whatsapp_parser import parse


SAMPLE = """[12/03/2024, 14:32] Alice: hey, are we still on for tomorrow?
[12/03/2024, 14:33] Bob: yes, 10am
multi-line continuation here
[12/03/2024, 14:35] Alice: cool"""


def test_parse_basic():
    msgs = list(parse(SAMPLE))
    assert len(msgs) == 3
    assert msgs[0].sender == "Alice"
    assert "10am" in msgs[1].body
    assert "continuation" in msgs[1].body


def test_parse_ignores_system_lines_and_parses_hyphen_format():
    sample = """28/06/2025, 02:10 - Messages and calls are end-to-end encrypted.
29/06/2022, 23:11 - Didi created group \"familia\"
29/06/2025, 14:59 - Mummy: Kya delete ki
29/06/2025, 16:52 - Didi: Heheheehe nhi batayungi
29/06/2025, 16:54 - Anant: Bacchiii"""

    msgs = list(parse(sample))
    assert len(msgs) == 3
    assert msgs[0].sender == "Mummy"
    assert msgs[1].sender == "Didi"
    assert msgs[2].body == "Bacchiii"

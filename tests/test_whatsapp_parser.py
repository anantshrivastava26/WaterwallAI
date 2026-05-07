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

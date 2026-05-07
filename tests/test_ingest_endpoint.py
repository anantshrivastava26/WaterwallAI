from fastapi.testclient import TestClient
from sqlalchemy import create_engine, delete, select
from sqlalchemy.orm import sessionmaker

from backend.app.db.models import Message
from backend.app.db.session import Base
from backend.app.main import app

SAMPLE = """[12/03/2024, 14:32] Alice: hey, are we still on for tomorrow?
[12/03/2024, 14:33] Bob: yes, 10am
multi-line continuation here
[12/03/2024, 14:35] Alice: cool"""


def _test_session_local(tmp_path):
    db_path = tmp_path / "test_ingest.sqlite"
    engine = create_engine(f"sqlite:///{db_path}", future=True)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, autoflush=False, autocommit=False)


def test_ingest_whatsapp_roundtrip_and_idempotent(monkeypatch, tmp_path):
    test_session_local = _test_session_local(tmp_path)

    import backend.app.api.ingest as ingest_api

    monkeypatch.setattr(ingest_api, "SessionLocal", test_session_local)

    client = TestClient(app)

    first = client.post(
        "/ingest/whatsapp",
        files={"file": ("chat.txt", SAMPLE.encode("utf-8"), "text/plain")},
    )
    assert first.status_code == 200
    assert first.json() == {"inserted": 3, "skipped": 0}

    with test_session_local() as session:
        count = len(session.scalars(select(Message)).all())
        assert count == 3

    second = client.post(
        "/ingest/whatsapp",
        files={"file": ("chat.txt", SAMPLE.encode("utf-8"), "text/plain")},
    )
    assert second.status_code == 200
    assert second.json() == {"inserted": 0, "skipped": 3}

    with test_session_local() as session:
        count = len(session.scalars(select(Message)).all())
        assert count == 3
        session.execute(delete(Message))
        session.commit()

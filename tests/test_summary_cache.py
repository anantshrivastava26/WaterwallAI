from datetime import datetime

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app.db.models import DailySummary, Message
from backend.app.db.session import Base
from backend.app.main import app


def _test_session_local(tmp_path):
    db_path = tmp_path / "test_summary.sqlite"
    engine = create_engine(f"sqlite:///{db_path}", future=True)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, autoflush=False, autocommit=False)


def test_daily_summary_is_cached(monkeypatch, tmp_path):
    test_session_local = _test_session_local(tmp_path)

    import backend.app.api.summary as summary_api

    monkeypatch.setattr(summary_api, "SessionLocal", test_session_local)

    calls = {"count": 0}

    def fake_summarize(_excerpts):
        calls["count"] += 1
        return "cached daily summary"

    monkeypatch.setattr(summary_api, "summarize_clusters", fake_summarize)

    target_day = datetime(2024, 3, 12)
    with test_session_local() as session:
        session.add(
            Message(
                id="m1",
                source="whatsapp",
                sender="Alice",
                timestamp=target_day.replace(hour=14, minute=30),
                message="Hello",
                embedding_id=None,
                priority_score=0.0,
                topics=[],
                entities=[],
                sentiment=None,
                summary=None,
            )
        )
        session.add(
            Message(
                id="m2",
                source="whatsapp",
                sender="Bob",
                timestamp=target_day.replace(hour=14, minute=31),
                message="Hi",
                embedding_id=None,
                priority_score=0.0,
                topics=[],
                entities=[],
                sentiment=None,
                summary=None,
            )
        )
        session.commit()

    client = TestClient(app)

    first = client.get("/summary/daily", params={"date": "2024-03-12"})
    assert first.status_code == 200
    assert first.json() == {"summary": "cached daily summary", "messages": 2}
    assert calls["count"] == 1

    second = client.get("/summary/daily", params={"date": "2024-03-12"})
    assert second.status_code == 200
    assert second.json() == {"summary": "cached daily summary", "messages": 2}
    assert calls["count"] == 1

    with test_session_local() as session:
        cached = session.get(DailySummary, target_day.date())
        assert cached is not None

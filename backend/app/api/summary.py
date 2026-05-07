from datetime import UTC, date, datetime, time, timedelta

from fastapi import APIRouter, Query
from sqlalchemy import select

from ai.summarizer import summarize_clusters
from backend.app.config import settings
from backend.app.db.models import DailySummary, Message
from backend.app.db.session import SessionLocal

router = APIRouter()


@router.get("/daily")
async def daily_summary(day: date | None = Query(default=None, alias="date")) -> dict:
    target_day = day or date.today()
    start_dt = datetime.combine(target_day, time.min)
    end_dt = start_dt + timedelta(days=1)

    with SessionLocal() as session:
        cached = session.get(DailySummary, target_day)
        messages = session.scalars(
            select(Message)
            .where(Message.timestamp >= start_dt, Message.timestamp < end_dt)
            .order_by(Message.timestamp.asc())
        ).all()

        if not messages:
            return {"summary": "", "messages": 0}

        if cached is not None:
            return {"summary": cached.body, "messages": len(messages)}

        trimmed = messages[-settings.max_context_messages :]
        excerpt = "\n".join(
            f"[{msg.timestamp.strftime('%H:%M')}] {msg.sender}: {msg.message}" for msg in trimmed
        )

        summary_text = summarize_clusters([excerpt])
        session.add(
            DailySummary(
                day=target_day,
                body=summary_text,
                model=settings.lm_studio_model,
                generated_at=datetime.now(UTC),
            )
        )
        session.commit()

    return {"summary": summary_text, "messages": len(messages)}


@router.get("/weekly")
async def weekly_summary() -> dict:
    raise NotImplementedError("Wire to ai.summarizer")

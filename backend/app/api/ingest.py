from datetime import datetime

from fastapi import APIRouter, BackgroundTasks, HTTPException, UploadFile

from backend.app.db.models import Message
from backend.app.db.session import SessionLocal
from backend.app.services.graphify_export import refresh as refresh_graph
from ingestion.normalizer import to_message_dict
from ingestion.whatsapp_parser import parse

router = APIRouter()


@router.post("/whatsapp")
async def ingest_whatsapp(file: UploadFile, background_tasks: BackgroundTasks) -> dict:
    if not file.filename or not file.filename.lower().endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt WhatsApp exports are supported")

    raw = await file.read()
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise HTTPException(status_code=400, detail="File must be UTF-8 encoded") from exc

    inserted = 0
    skipped = 0
    seen_ids: set[str] = set()

    with SessionLocal() as session:
        for parsed in parse(text):
            row = to_message_dict("whatsapp", parsed.sender, parsed.timestamp, parsed.body)
            row["timestamp"] = datetime.fromisoformat(row["timestamp"])
            message_id = row["id"]

            # Avoid duplicate primary keys in the same request payload.
            if message_id in seen_ids:
                skipped += 1
                continue
            seen_ids.add(message_id)

            if session.get(Message, message_id) is None:
                inserted += 1
                session.add(Message(**row))
            else:
                skipped += 1

        session.commit()

    if inserted > 0:
        background_tasks.add_task(refresh_graph)

    return {"inserted": inserted, "skipped": skipped}


@router.post("/email")
async def ingest_email(file: UploadFile) -> dict:
    raise NotImplementedError("Wire to ingestion.email_parser")

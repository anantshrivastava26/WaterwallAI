from datetime import datetime

from fastapi import APIRouter, HTTPException, UploadFile

from backend.app.db.models import Message
from backend.app.db.session import SessionLocal
from ingestion.normalizer import to_message_dict
from ingestion.whatsapp_parser import parse

router = APIRouter()


@router.post("/whatsapp")
async def ingest_whatsapp(file: UploadFile) -> dict:
    if not file.filename or not file.filename.lower().endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt WhatsApp exports are supported")

    raw = await file.read()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise HTTPException(status_code=400, detail="File must be UTF-8 encoded") from exc

    inserted = 0
    skipped = 0

    with SessionLocal() as session:
        for parsed in parse(text):
            row = to_message_dict("whatsapp", parsed.sender, parsed.timestamp, parsed.body)
            row["timestamp"] = datetime.fromisoformat(row["timestamp"])

            if session.get(Message, row["id"]) is None:
                inserted += 1
            else:
                skipped += 1

            session.merge(Message(**row))

        session.commit()

    return {"inserted": inserted, "skipped": skipped}


@router.post("/email")
async def ingest_email(file: UploadFile) -> dict:
    raise NotImplementedError("Wire to ingestion.email_parser")

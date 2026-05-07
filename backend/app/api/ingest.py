from fastapi import APIRouter, UploadFile

router = APIRouter()


@router.post("/whatsapp")
async def ingest_whatsapp(file: UploadFile) -> dict:
    raise NotImplementedError("Wire to ingestion.whatsapp_parser")


@router.post("/email")
async def ingest_email(file: UploadFile) -> dict:
    raise NotImplementedError("Wire to ingestion.email_parser")

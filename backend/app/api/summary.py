from fastapi import APIRouter

router = APIRouter()


@router.get("/daily")
async def daily_summary() -> dict:
    raise NotImplementedError("Wire to ai.summarizer")


@router.get("/weekly")
async def weekly_summary() -> dict:
    raise NotImplementedError("Wire to ai.summarizer")

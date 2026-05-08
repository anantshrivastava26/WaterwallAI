from fastapi import APIRouter

from backend.app.services.graphify_export import refresh
from backend.app.services.message_correlation import build_message_correlation_graph

router = APIRouter()


@router.post("/refresh")
def refresh_graph() -> dict:
    return refresh()


@router.post("/message-correlation")
def build_message_graph() -> dict:
    return build_message_correlation_graph()

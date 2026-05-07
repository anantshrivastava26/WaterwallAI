from fastapi import APIRouter

from backend.app.services.graphify_export import refresh

router = APIRouter()


@router.post("/refresh")
def refresh_graph() -> dict:
    return refresh()

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class SearchRequest(BaseModel):
    query: str
    top_k: int = 10


@router.post("")
async def semantic_search(req: SearchRequest) -> dict:
    raise NotImplementedError("Wire to embeddings + qdrant")

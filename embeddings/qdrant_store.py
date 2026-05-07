"""Qdrant client wrapper for semantic retrieval."""
from __future__ import annotations

from functools import lru_cache

from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, PointStruct, VectorParams

from backend.app.config import settings


@lru_cache(maxsize=1)
def client() -> QdrantClient:
    return QdrantClient(url=settings.qdrant_url)


def ensure_collection() -> None:
    c = client()
    if settings.qdrant_collection in {col.name for col in c.get_collections().collections}:
        return
    c.create_collection(
        collection_name=settings.qdrant_collection,
        vectors_config=VectorParams(size=settings.embedding_dim, distance=Distance.COSINE),
    )


def upsert(ids: list[str], vectors: list[list[float]], payloads: list[dict]) -> None:
    points = [PointStruct(id=i, vector=v, payload=p) for i, v, p in zip(ids, vectors, payloads)]
    client().upsert(collection_name=settings.qdrant_collection, points=points)


def search(vector: list[float], top_k: int = 10) -> list[dict]:
    hits = client().search(
        collection_name=settings.qdrant_collection, query_vector=vector, limit=top_k
    )
    return [{"id": h.id, "score": h.score, "payload": h.payload} for h in hits]

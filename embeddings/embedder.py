"""Local embedding generation (section 7). Dedicated model, NOT the chat LLM."""
from __future__ import annotations

from functools import lru_cache

from backend.app.config import settings


@lru_cache(maxsize=1)
def _model():
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(settings.embedding_model)


def embed(texts: list[str]) -> list[list[float]]:
    vectors = _model().encode(texts, normalize_embeddings=True, show_progress_bar=False)
    return vectors.tolist()

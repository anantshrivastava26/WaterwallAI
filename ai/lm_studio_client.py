"""Thin LM Studio wrapper. LM Studio exposes an OpenAI-compatible API."""
from __future__ import annotations

from openai import OpenAI

from backend.app.config import settings


def client() -> OpenAI:
    return OpenAI(base_url=settings.lm_studio_base_url, api_key=settings.lm_studio_api_key)


def chat(
    system: str,
    user: str,
    *,
    temperature: float = 0.2,
    max_tokens: int = 512,
) -> str:
    resp = client().chat.completions.create(
        model=settings.lm_studio_model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return resp.choices[0].message.content or ""

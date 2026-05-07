"""Thin LM Studio wrapper using the native v1 REST API (/api/v1/chat)."""
from __future__ import annotations

import httpx

from backend.app.config import settings


def chat(
    system: str,
    user: str,
    *,
    temperature: float = 0.2,
    max_tokens: int = 512,
) -> str:
    payload = {
        "model": settings.lm_studio_model,
        "input": user,
        "system_prompt": system,
        "temperature": temperature,
        "max_output_tokens": max_tokens,
        "stream": False,
    }
    headers = {"Content-Type": "application/json"}
    if settings.lm_studio_api_key:
        headers["Authorization"] = f"Bearer {settings.lm_studio_api_key}"

    base = settings.lm_studio_base_url.rstrip("/")
    with httpx.Client(timeout=120.0) as http:
        response = http.post(f"{base}/api/v1/chat", json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

    parts = [
        item.get("content", "")
        for item in data.get("output", [])
        if item.get("type") == "message"
    ]
    return "\n".join(p for p in parts if p)

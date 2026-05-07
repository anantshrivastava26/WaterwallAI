"""Normalize parser output to the unified Message entity (section 12)."""
from __future__ import annotations

import hashlib
from datetime import datetime
from typing import Any


def make_id(source: str, sender: str, ts: datetime, body: str) -> str:
    h = hashlib.sha1(f"{source}|{sender}|{ts.isoformat()}|{body}".encode()).hexdigest()
    return f"{source}_{h[:16]}"


def to_message_dict(
    source: str,
    sender: str,
    ts: datetime,
    body: str,
) -> dict[str, Any]:
    return {
        "id": make_id(source, sender, ts, body),
        "source": source,
        "sender": sender,
        "timestamp": ts.isoformat(),
        "message": body,
        "embedding_id": None,
        "priority_score": 0.0,
        "topics": [],
        "entities": [],
        "sentiment": None,
        "summary": None,
    }

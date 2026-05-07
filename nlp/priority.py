"""Deterministic priority scoring engine (section 14)."""
from __future__ import annotations

from datetime import datetime, timezone

from .extractors import detect_urgency


def recency_weight(ts: datetime, now: datetime | None = None) -> float:
    now = now or datetime.now(timezone.utc)
    age_hours = max(0.0, (now - ts).total_seconds() / 3600.0)
    return max(0.0, 1.0 - age_hours / 168.0)


def sender_weight(sender: str, frequent_contacts: set[str]) -> float:
    return 1.0 if sender in frequent_contacts else 0.3


def project_weight(text: str, active_project_terms: set[str]) -> float:
    lower = text.lower()
    return 1.0 if any(t in lower for t in active_project_terms) else 0.0


def score(
    text: str,
    ts: datetime,
    sender: str,
    frequent_contacts: set[str],
    active_project_terms: set[str],
    emotional: float = 0.0,
) -> float:
    return (
        0.30 * recency_weight(ts)
        + 0.25 * sender_weight(sender, frequent_contacts)
        + 0.20 * detect_urgency(text)
        + 0.10 * emotional
        + 0.15 * project_weight(text, active_project_terms)
    )

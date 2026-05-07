"""Lightweight NLP layer (section 6). spaCy + regex, no LLM."""
from __future__ import annotations

import re

URGENCY_TERMS = {"urgent", "asap", "deadline", "important", "today", "now"}


def detect_urgency(text: str) -> float:
    lower = text.lower()
    hits = sum(1 for t in URGENCY_TERMS if t in lower)
    return min(1.0, hits / 3.0)


def extract_entities(text: str) -> list[dict]:
    raise NotImplementedError("Wire to spaCy en_core_web_sm")


def detect_topics(text: str) -> list[str]:
    raise NotImplementedError("Use embeddings + cluster centroids")


URL_RE = re.compile(r"https?://\S+")


def extract_urls(text: str) -> list[str]:
    return URL_RE.findall(text)

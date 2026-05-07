"""Deterministic .eml / mbox parser placeholder."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from email import policy
from email.parser import BytesParser
from typing import Iterator


@dataclass
class ParsedEmail:
    message_id: str
    sender: str
    recipients: list[str]
    subject: str
    timestamp: datetime | None
    body: str


def parse_eml(raw: bytes) -> ParsedEmail:
    msg = BytesParser(policy=policy.default).parsebytes(raw)
    body_part = msg.get_body(preferencelist=("plain", "html"))
    body = body_part.get_content() if body_part else ""
    return ParsedEmail(
        message_id=msg.get("Message-ID", ""),
        sender=str(msg.get("From", "")),
        recipients=[r.strip() for r in str(msg.get("To", "")).split(",") if r.strip()],
        subject=str(msg.get("Subject", "")),
        timestamp=msg.get("Date").datetime if msg.get("Date") else None,
        body=body,
    )


def parse_mbox(path: str) -> Iterator[ParsedEmail]:
    raise NotImplementedError("Implement mbox iteration")

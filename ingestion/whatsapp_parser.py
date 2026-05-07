"""Deterministic WhatsApp TXT export parser. No LLM."""
from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from typing import Iterator

LINE_RE = re.compile(
    r"^\[?(?P<ts>\d{1,2}/\d{1,2}/\d{2,4},?\s+\d{1,2}:\d{2}(?::\d{2})?\s*(?:AM|PM)?)\]?\s*[-:]?\s*"
    r"(?P<sender>[^:]+?):\s*(?P<body>.*)$"
)


@dataclass
class ParsedMessage:
    timestamp: datetime
    sender: str
    body: str


def _parse_ts(raw: str) -> datetime | None:
    for fmt in (
        "%d/%m/%Y, %H:%M",
        "%d/%m/%y, %H:%M",
        "%m/%d/%y, %I:%M %p",
        "%m/%d/%Y, %I:%M %p",
        "%d/%m/%Y, %H:%M:%S",
    ):
        try:
            return datetime.strptime(raw.strip(), fmt)
        except ValueError:
            continue
    return None


def parse(text: str) -> Iterator[ParsedMessage]:
    current: ParsedMessage | None = None
    for line in text.splitlines():
        m = LINE_RE.match(line)
        if m:
            if current is not None:
                yield current
            ts = _parse_ts(m.group("ts"))
            if ts is None:
                current = None
                continue
            current = ParsedMessage(
                timestamp=ts,
                sender=m.group("sender").strip(),
                body=m.group("body").strip(),
            )
        elif current is not None:
            current.body += "\n" + line
    if current is not None:
        yield current

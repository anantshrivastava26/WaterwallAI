"""Private knowledge-graph export of ingested messages.

Dumps the messages table into per-source/per-month markdown files under
``data/graphify-data/``, then extracts semantic entities and relationships
to build a knowledge graph at ``data/graphify-data/graphify-out/``.
The whole tree lives under ``data/``, which is gitignored, so nothing is published.
"""
from __future__ import annotations

import logging
from collections import defaultdict
from pathlib import Path

from sqlalchemy import select

from backend.app.db.models import Message
from backend.app.db.session import SessionLocal
from backend.app.services.semantic_extractor import extract_semantic_graph

log = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[3]
GRAPH_DIR = PROJECT_ROOT / "data" / "graphify-data"
GRAPH_OUT = GRAPH_DIR / "graphify-out"


def regenerate_inputs() -> dict:
    """Rewrite per-source/per-month markdown dumps from the messages table."""
    GRAPH_DIR.mkdir(parents=True, exist_ok=True)

    buckets: dict[tuple[str, str], list[Message]] = defaultdict(list)
    with SessionLocal() as session:
        rows = session.scalars(select(Message).order_by(Message.timestamp.asc())).all()
        for msg in rows:
            key = (msg.source, msg.timestamp.strftime("%Y-%m"))
            buckets[key].append(msg)

    written: list[str] = []
    for (source, ym), msgs in buckets.items():
        source_dir = GRAPH_DIR / source
        source_dir.mkdir(parents=True, exist_ok=True)
        path = source_dir / f"{ym}.md"
        tmp = path.with_suffix(".md.tmp")
        with tmp.open("w", encoding="utf-8") as fh:
            fh.write(f"# {source} — {ym}\n\n")
            for m in msgs:
                stamp = m.timestamp.isoformat(timespec="minutes")
                fh.write(f"[{stamp}] {m.sender}: {m.message}\n")
        tmp.replace(path)
        written.append(str(path.relative_to(PROJECT_ROOT)))

    return {"messages": sum(len(v) for v in buckets.values()), "files": written}


def run_graphify_extract() -> dict:
    """Build semantic knowledge graph using spaCy entity extraction."""
    GRAPH_OUT.mkdir(parents=True, exist_ok=True)
    log.info("Extracting semantic graph from messages")

    try:
        result = extract_semantic_graph()
        return {
            "ok": result["ok"],
            "mode": "semantic-spacy",
            "nodes": result.get("nodes", 0),
            "edges": result.get("edges", 0),
            "graph_dir": str(GRAPH_OUT.relative_to(PROJECT_ROOT)),
            "graph_file": result.get("graph_file"),
        }
    except Exception as e:
        log.exception("Failed to extract semantic graph")
        return {
            "ok": False,
            "error": str(e),
            "graph_dir": str(GRAPH_OUT.relative_to(PROJECT_ROOT)),
        }


def refresh() -> dict:
    return {"inputs": regenerate_inputs(), "extract": run_graphify_extract()}

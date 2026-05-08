"""Extract entities and relationships from messages using spaCy.

Builds a semantic knowledge graph from ingested messages by identifying:
- Named entities (people, organizations, locations, events)
- Entity co-mentions (entities mentioned together in messages)
- Temporal patterns (entities appearing in specific time periods)
"""
from __future__ import annotations

import json
import logging
from collections import defaultdict
from pathlib import Path

import spacy
from sqlalchemy import select

from backend.app.db.models import Message
from backend.app.db.session import SessionLocal

log = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[3]
GRAPH_DIR = PROJECT_ROOT / "data" / "graphify-data"
GRAPH_OUT = GRAPH_DIR / "graphify-out"
GRAPH_FILE = GRAPH_OUT / "graph.json"


def _get_nlp():
    """Load spaCy model for NER."""
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        log.warning("en_core_web_sm not found, attempting download")
        import subprocess

        subprocess.run(
            ["python", "-m", "spacy", "download", "en_core_web_sm"],
            check=True,
        )
        nlp = spacy.load("en_core_web_sm")
    return nlp


def _normalize_id(label: str) -> str:
    """Convert a label to a graph node ID."""
    return label.lower().replace(" ", "_").replace("-", "_").replace(".", "_")


def extract_semantic_graph() -> dict:
    """Extract entities and relationships from messages, build knowledge graph."""
    GRAPH_OUT.mkdir(parents=True, exist_ok=True)

    nlp = _get_nlp()

    nodes = {}
    edges = []
    entity_mentions = defaultdict(list)  # entity -> list of (source, month)
    entity_cooccurrences = defaultdict(set)  # (entity1, entity2) -> count

    with SessionLocal() as session:
        messages = session.scalars(select(Message).order_by(Message.timestamp.asc())).all()

        for msg in messages:
            month_key = msg.timestamp.strftime("%Y-%m")
            doc = nlp(msg.message)

            for ent in doc.ents:
                if ent.label_ in {"PERSON", "ORG", "GPE", "EVENT", "PRODUCT"}:
                    entity_text = ent.text.strip()
                    entity_type = ent.label_
                    entity_id = _normalize_id(f"{entity_text}_{entity_type}")

                    if entity_id not in nodes:
                        nodes[entity_id] = {
                            "label": f"{entity_text} ({entity_type})",
                            "file_type": "entity",
                            "entity_type": entity_type,
                            "source_file": f"{msg.source}/{month_key}.md",
                            "source_location": "L0",
                            "id": entity_id,
                            "community": 0,
                            "norm_label": entity_text,
                        }

                    entity_mentions[entity_id].append((msg.source, month_key))

            # Extract entity co-occurrences
            entities = [
                (ent.text.strip(), ent.label_)
                for ent in doc.ents
                if ent.label_ in {"PERSON", "ORG", "GPE", "EVENT", "PRODUCT"}
            ]
            for i, (e1_text, e1_label) in enumerate(entities):
                for e2_text, e2_label in entities[i + 1 :]:
                    e1_id = _normalize_id(f"{e1_text}_{e1_label}")
                    e2_id = _normalize_id(f"{e2_text}_{e2_label}")
                    key = tuple(sorted([e1_id, e2_id]))
                    entity_cooccurrences[key].add((msg.source, month_key))

    # Create edges from entity co-occurrences
    for (e1_id, e2_id), occurrences in entity_cooccurrences.items():
        if e1_id in nodes and e2_id in nodes:
            weight = len(occurrences)
            edges.append(
                {
                    "relation": "co-mentioned",
                    "confidence": "EXTRACTED",
                    "source_file": "semantic",
                    "source_location": "L0",
                    "weight": min(weight / 10.0, 1.0),
                    "source": e1_id,
                    "target": e2_id,
                    "confidence_score": min(weight / 10.0, 1.0),
                }
            )

    # Create edges from entities to their time periods
    for entity_id, mentions in entity_mentions.items():
        unique_months = set(month for _, month in mentions)
        for month in unique_months:
            month_id = _normalize_id(month)
            if month_id not in nodes:
                nodes[month_id] = {
                    "label": month,
                    "file_type": "timeperiod",
                    "source_file": "semantic",
                    "source_location": "L0",
                    "id": month_id,
                    "community": 0,
                    "norm_label": month,
                }

            edges.append(
                {
                    "relation": "mentioned_in",
                    "confidence": "EXTRACTED",
                    "source_file": "semantic",
                    "source_location": "L0",
                    "weight": 1.0,
                    "source": entity_id,
                    "target": month_id,
                    "confidence_score": 1.0,
                }
            )

    # Assign communities based on entity type
    entity_type_to_community = {
        "PERSON": 1,
        "ORG": 2,
        "GPE": 3,
        "EVENT": 4,
        "PRODUCT": 5,
    }
    for node_id, node in nodes.items():
        if node["file_type"] == "entity":
            node["community"] = entity_type_to_community.get(node["entity_type"], 0)

    # Build graph structure
    graph = {
        "directed": False,
        "multigraph": False,
        "graph": {},
        "nodes": list(nodes.values()),
        "links": edges,
        "hyperedges": [],
        "built_at_commit": "semantic",
    }

    # Write graph to file
    with GRAPH_FILE.open("w", encoding="utf-8") as f:
        json.dump(graph, f, indent=2)

    log.info(
        "Semantic graph extracted: %d nodes, %d edges",
        len(nodes),
        len(edges),
    )

    return {
        "ok": True,
        "nodes": len(nodes),
        "edges": len(edges),
        "graph_file": str(GRAPH_FILE.relative_to(PROJECT_ROOT)),
    }

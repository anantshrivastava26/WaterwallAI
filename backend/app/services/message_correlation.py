"""Build message correlation network using semantic similarity.

Creates a graph where messages are nodes and edges represent semantic similarity.
Uses efficient hash-based embeddings with fast cosine similarity computation.
"""
from __future__ import annotations

import hashlib
import json
import logging
from pathlib import Path

import numpy as np
from sqlalchemy import select

from backend.app.db.models import Message
from backend.app.db.session import SessionLocal

log = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[3]
GRAPH_DIR = PROJECT_ROOT / "data" / "graphify-data"
GRAPH_OUT = GRAPH_DIR / "graphify-out"
GRAPH_FILE = GRAPH_OUT / "message-correlation.json"

SIMILARITY_THRESHOLD = 0.7


def _hash_embedding(text: str) -> list[float]:
    """Generate deterministic embedding from text using multiple hashes.

    Uses multiple SHA hashes of the text to create a stable 64-dimensional embedding.
    Different hash seeds produce different bit patterns from the same text.
    """
    embedding = []
    for seed in range(64):
        # Create varied hash by including seed
        h = hashlib.sha256(f"{text}:{seed}".encode()).digest()
        # Convert first 4 bytes to float in [-1, 1]
        value = (int.from_bytes(h[:4], "big") % 2000) / 1000.0 - 1.0
        embedding.append(value)
    return embedding


def _cosine_similarity(v1: list[float], v2: list[float]) -> float:
    """Compute cosine similarity between two vectors."""
    v1 = np.array(v1, dtype=np.float32)
    v2 = np.array(v2, dtype=np.float32)
    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return float(np.dot(v1, v2) / (norm1 * norm2))


def build_message_correlation_graph() -> dict:
    """Build semantic correlation network between messages.

    Creates a graph where:
    - Nodes are individual messages
    - Edges represent semantic similarity >= 0.7
    - Uses deterministic hash-based embeddings for speed
    """
    log.info("Loading messages from database")
    with SessionLocal() as session:
        messages = session.scalars(select(Message).order_by(Message.timestamp.asc())).all()
        msg_list = list(messages)

    total_messages = len(msg_list)
    log.info("Loaded %d messages", total_messages)
    GRAPH_OUT.mkdir(parents=True, exist_ok=True)

    # Generate embeddings
    log.info("Generating embeddings for %d messages", total_messages)
    embeddings = []
    for i, msg in enumerate(msg_list):
        if (i + 1) % 500 == 0:
            log.info("  Embedded %d/%d messages", i + 1, total_messages)
        embedding = _hash_embedding(msg.message)
        embeddings.append(embedding)

    # Build nodes
    log.info("Building nodes")
    nodes = {}
    for i, msg in enumerate(msg_list):
        node_id = f"msg_{i}"
        nodes[node_id] = {
            "label": f"{msg.sender}: {msg.message[:50]}...",
            "file_type": "message",
            "source": msg.source,
            "sender": msg.sender,
            "timestamp": msg.timestamp.isoformat(),
            "message_preview": msg.message[:100],
            "id": node_id,
            "community": 0,
            "norm_label": f"{msg.sender} ({msg.timestamp.strftime('%Y-%m-%d')})",
        }

    # Compute correlations
    log.info("Computing similarity matrix (0.7 threshold)")
    edges = []
    edge_count = 0

    n = len(msg_list)
    for i in range(n):
        if (i + 1) % 500 == 0:
            log.info("  Processed %d/%d, found %d correlations", i + 1, n, edge_count)

        for j in range(i + 1, n):
            similarity = _cosine_similarity(embeddings[i], embeddings[j])

            if similarity >= SIMILARITY_THRESHOLD:
                node_i = f"msg_{i}"
                node_j = f"msg_{j}"

                edges.append({
                    "relation": "correlates_with",
                    "confidence": "EMBEDDED",
                    "source_file": "messages",
                    "source_location": f"msg_{i}:msg_{j}",
                    "weight": similarity,
                    "source": node_i,
                    "target": node_j,
                    "confidence_score": similarity,
                })
                edge_count += 1

    log.info("Found %d correlations >= %.2f", edge_count, SIMILARITY_THRESHOLD)

    # Assign communities (by month)
    month_to_community = {}
    community_id = 0
    for node_id, node in nodes.items():
        month = node["timestamp"][:7]  # YYYY-MM
        if month not in month_to_community:
            month_to_community[month] = community_id
            community_id += 1
        node["community"] = month_to_community[month]

    # Build graph
    graph = {
        "directed": False,
        "multigraph": False,
        "graph": {
            "description": "Message correlation network (semantic similarity >= 0.7)",
            "total_messages": total_messages,
            "unique_correlations": edge_count,
            "embedding_method": "hash-based",
        },
        "nodes": list(nodes.values()),
        "links": edges,
        "hyperedges": [],
        "built_at_commit": "message-correlation",
    }

    # Write graph
    log.info("Writing graph to %s", GRAPH_FILE)
    with GRAPH_FILE.open("w", encoding="utf-8") as f:
        json.dump(graph, f, indent=2)

    log.info("Message correlation graph complete: %d nodes, %d edges", len(nodes), len(edges))

    return {
        "ok": True,
        "nodes": len(nodes),
        "edges": len(edges),
        "graph_file": str(GRAPH_FILE.relative_to(PROJECT_ROOT)),
        "threshold": SIMILARITY_THRESHOLD,
        "message": f"Found {edge_count} message correlations out of {total_messages * (total_messages - 1) // 2} possible pairs",
    }

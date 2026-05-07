"""Deterministic graph edge generation. No LLM."""
from __future__ import annotations

from collections import Counter

from .neo4j_client import session
from .schema import EdgeType, NodeLabel


def upsert_person_topic(person: str, topic: str, weight: int = 1) -> None:
    with session() as s:
        s.run(
            f"""
            MERGE (p:{NodeLabel.PERSON} {{name: $person}})
            MERGE (t:{NodeLabel.TOPIC} {{name: $topic}})
            MERGE (p)-[r:{EdgeType.DISCUSSED}]->(t)
            ON CREATE SET r.weight = $weight
            ON MATCH SET r.weight = coalesce(r.weight, 0) + $weight
            """,
            person=person,
            topic=topic,
            weight=weight,
        )


def build_frequent_contacts(pairs: list[tuple[str, str]], min_count: int = 5) -> None:
    counts = Counter(tuple(sorted(p)) for p in pairs)
    with session() as s:
        for (a, b), n in counts.items():
            if n < min_count:
                continue
            s.run(
                f"""
                MERGE (x:{NodeLabel.PERSON} {{name: $a}})
                MERGE (y:{NodeLabel.PERSON} {{name: $b}})
                MERGE (x)-[r:{EdgeType.FREQUENTLY_CONTACTS}]-(y)
                SET r.count = $n
                """,
                a=a,
                b=b,
                n=n,
            )

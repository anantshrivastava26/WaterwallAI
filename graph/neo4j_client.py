"""Neo4j driver wrapper."""
from __future__ import annotations

from contextlib import contextmanager
from functools import lru_cache

from neo4j import Driver, GraphDatabase

from backend.app.config import settings

from .schema import CONSTRAINTS_CYPHER


@lru_cache(maxsize=1)
def driver() -> Driver:
    return GraphDatabase.driver(
        settings.neo4j_uri, auth=(settings.neo4j_user, settings.neo4j_password)
    )


@contextmanager
def session():
    with driver().session() as s:
        yield s


def init_constraints() -> None:
    with session() as s:
        for stmt in CONSTRAINTS_CYPHER:
            s.run(stmt)

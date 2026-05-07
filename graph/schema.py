"""Neo4j graph schema (section 13)."""
from __future__ import annotations

from enum import Enum


class NodeLabel(str, Enum):
    PERSON = "Person"
    TOPIC = "Topic"
    TASK = "Task"
    EVENT = "Event"
    EMOTION = "Emotion"
    CONVERSATION = "Conversation"
    MESSAGE = "Message"


class EdgeType(str, Enum):
    DISCUSSED = "DISCUSSED"
    ASSIGNED = "ASSIGNED"
    RELATED_TO = "RELATED_TO"
    CONTAINS = "CONTAINS"
    FREQUENTLY_CONTACTS = "FREQUENTLY_CONTACTS"
    MENTIONS = "MENTIONS"


CONSTRAINTS_CYPHER: list[str] = [
    "CREATE CONSTRAINT person_name IF NOT EXISTS FOR (p:Person) REQUIRE p.name IS UNIQUE",
    "CREATE CONSTRAINT topic_name IF NOT EXISTS FOR (t:Topic) REQUIRE t.name IS UNIQUE",
    "CREATE CONSTRAINT message_id IF NOT EXISTS FOR (m:Message) REQUIRE m.id IS UNIQUE",
]

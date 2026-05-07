# Phase 3 — Graph Intelligence

**Duration:** 3 weeks. **Blueprint reference:** §13 Graph Schema, §15 Epic Relationship Graph, §16 Phase 3.

## Goal

End of phase: messages produce typed nodes (`Person`, `Topic`, `Task`, `Event`, `Emotion`) and edges (`DISCUSSED`, `ASSIGNED`, `RELATED_TO`, `CONTAINS`, `FREQUENTLY_CONTACTS`) in Neo4j. A user can query "who do I talk to most about Project X?" via Cypher.

## Pre-requisites

- Phase 2 done (embeddings live)
- Neo4j container running ([CONFIGURATION.md](CONFIGURATION.md) §5)
- spaCy English model installed: `python -m spacy download en_core_web_sm`

## Configuration changes

| Var | Notes |
|---|---|
| `NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD` | confirm match docker-compose |
| Add `SPACY_MODEL=en_core_web_sm` to `.env` and `Settings` | extractor module reads this |

## Execution steps

### 3.1 Initialize Neo4j constraints

```powershell
python -c "from graph.neo4j_client import init_constraints; init_constraints()"
```

This runs the `CREATE CONSTRAINT` statements in [graph/schema.py](../graph/schema.py). Idempotent.

### 3.2 Entity extraction (deterministic, no LLM)

Implement [nlp/extractors.py](../nlp/extractors.py) `extract_entities`:

- Load spaCy lazily via `lru_cache`, same pattern as `embeddings.embedder._model`
- Run `nlp(text).ents`
- Map spaCy labels to graph node types:
  - `PERSON` → `Person`
  - `ORG`, `PRODUCT`, `WORK_OF_ART` → `Topic`
  - `DATE`, `TIME`, `EVENT` → `Event`
  - `MONEY`, `PERCENT` → annotate but don't create nodes (noise)
- Return `[{type, text, start, end, confidence: 1.0}]`

For **task detection** add a regex pre-pass:
- `r"\b(remind me to|todo|to do|need to|don't forget to|please)\b\s+(.+?)(?:[.!?]|$)"` → `Task` node
- Imperative-mood detection via spaCy POS (verb at sentence start) → also `Task`

For **topic detection** (blueprint §6 mentions it as a separate step): defer until P4. For P3 just rely on NER `ORG`/`PRODUCT` and keep a TODO.

### 3.3 Edge generation pipeline

In a new module `graph/builder_pipeline.py`:

```
def index_message(msg: Message) -> None:
    ents = extract_entities(msg.message)
    with session() as s:
        upsert_message_node(s, msg)
        upsert_person_node(s, msg.sender)
        s.run(MERGE Person)-[:SENT]->(Message)
        for ent in ents:
            if ent.type == 'Topic':
                upsert_person_topic(msg.sender, ent.text)
            elif ent.type == 'Task':
                upsert_message_task(msg.id, ent.text)
            elif ent.type == 'Person' and ent.text != msg.sender:
                # mention edge
                ...
```

Wire this into the ingest pipeline AFTER the embedding upsert. So per message:
SQLite insert → embed → Qdrant upsert → graph indexing. All synchronous in P3; we'll move heavy steps to a worker queue in P4.

### 3.4 FREQUENTLY_CONTACTS aggregation

This is a reduce, not a per-message edge. Run nightly (or on-demand from an admin endpoint):

- Pull all `(sender, mentioned_person)` pairs from the last 30 days
- Count co-occurrences
- Call `graph.edge_builder.build_frequent_contacts(pairs, min_count=5)`

Add a scheduler job stub in [scheduler/jobs.py](../scheduler/jobs.py) `graph_refresh_job` (already a stub).

### 3.5 Graph query API

Add `/graph` routes in `backend/app/api/graph.py`:

| Endpoint | Returns |
|---|---|
| `GET /graph/people?top=20` | top contacts by message count |
| `GET /graph/topics?top=20` | top topics by mention count |
| `GET /graph/person/{name}/topics` | topics a given person discusses, with weights |
| `GET /graph/topic/{name}/people` | people who discuss a given topic |
| `GET /graph/path?from=A&to=B&max_hops=4` | shortest path between two nodes |

Each handler is a single Cypher query. Keep responses small (<200 nodes) — frontend pagination is fine.

### 3.6 Backfill graph from existing messages

`scripts/backfill_graph.py`:

- Iterate all messages
- Run `index_message` for each
- Idempotent because every Cypher call uses `MERGE`

## User stories satisfied

- **Epic: Relationship Graph** — Dynamic graph, topic clusters, person nodes

## Tests

| Test | What it asserts |
|---|---|
| `tests/test_extractors.py` | spaCy detects known entities; regex catches "remind me to ..." |
| `tests/test_graph_roundtrip.py` | indexing a message produces expected nodes/edges (use Neo4j testcontainer or aiotestcontainers) |
| `tests/test_frequent_contacts.py` | given fixture pairs, builder emits correct edges with `min_count` honored |

## Definition of done

- [ ] Every message produces ≥1 node (the `Message` itself) and edges to its sender
- [ ] Cypher: `MATCH (p:Person)-[:DISCUSSED]->(t:Topic) RETURN p,t LIMIT 25` returns real data
- [ ] `/graph/path` finds a path between two real people who share a topic in <500ms
- [ ] Backfill script is restartable
- [ ] P1/P2 endpoints still pass

## Watch-outs

- **NER is noisy.** spaCy labels "Tomorrow" as `DATE` and "Sunday" as `DATE`. Consider a stop-list of common temporal-words you don't want as graph nodes.
- **Casing matters in Neo4j MERGE.** Normalize `Person.name` to `.lower().strip()` before MERGE or you'll get "Alice" and "alice" as two nodes.
- **Don't run NLP on every message synchronously.** spaCy is ~5–20ms per message; a 10k import is 1–3 minutes. Add a progress log every 500 messages.

## Out of scope

LLM-based topic naming, sentiment analysis, communication-pattern analytics, graph visualization (P5).

# Graph Report - WaterwallAI  (2026-05-08)

## Corpus Check
- 49 files · ~17,329 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 493 nodes · 529 edges · 56 communities (52 shown, 4 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 44 edges (avg confidence: 0.83)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d41eb73f`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 42|Community 42]]

## God Nodes (most connected - your core abstractions)
1. `Embedding Layer` - 11 edges
2. `Phase 2 — Semantic Layer` - 10 edges
3. `Phase 3 — Graph Intelligence` - 10 edges
4. `Phase 4 — Intelligence Engine` - 10 edges
5. `Graph Report - .graphify_input  (2026-05-08)` - 10 edges
6. `Communities (9 total, 0 thin omitted)` - 10 edges
7. `Configuration & Host Setup` - 9 edges
8. `Phase 1 — Foundation` - 9 edges
9. `Phase 5 — Frontend UX` - 9 edges
10. `Phase 6 — Production Hardening` - 9 edges

## Surprising Connections (you probably didn't know these)
- `test_parse_basic()` --calls--> `parse()`  [INFERRED]
  tests/test_whatsapp_parser.py → ingestion/whatsapp_parser.py
- `daily_summary()` --calls--> `summarize_clusters()`  [INFERRED]
  backend/app/api/summary.py → ai/summarizer.py
- `ingest_whatsapp()` --calls--> `parse()`  [INFERRED]
  backend/app/api/ingest.py → ingestion/whatsapp_parser.py
- `ingest_whatsapp()` --calls--> `to_message_dict()`  [INFERRED]
  backend/app/api/ingest.py → ingestion/normalizer.py
- `test_daily_summary_is_cached()` --calls--> `Message`  [INFERRED]
  tests/test_summary_cache.py → backend/app/db/models.py

## Hyperedges (group relationships)
- **Data Sources participating in Ingestion** — blueprint_whatsapp, blueprint_email, blueprint_notes, blueprint_docs_pdfs, blueprint_ingestion_layer [EXTRACTED 1.00]
- **Storage Architecture Backends** — blueprint_sqlite, blueprint_qdrant, blueprint_neo4j, blueprint_storage_layer [EXTRACTED 1.00]
- **Phase-Wise Execution Plan** — blueprint_phase_1, blueprint_phase_2, blueprint_phase_3, blueprint_phase_4, blueprint_phase_5, blueprint_phase_6 [EXTRACTED 1.00]

## Communities (56 total, 4 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (61): AI Budgeting System, AI Reasoning Layer, APScheduler, AsyncIO, Backend Stack, BGE-small, Cold Memory, Data Sources (+53 more)

### Community 1 - "Community 1"
Cohesion: 0.08
Nodes (25): 15. User Stories, Acceptance Criteria, Acceptance Criteria, Acceptance Criteria, Acceptance Criteria, Acceptance Criteria, Acceptance Criteria, Acceptance Criteria (+17 more)

### Community 2 - "Community 2"
Cohesion: 0.08
Nodes (25): 16. Phase-Wise Execution Plan, Deliverables, Deliverables, Deliverables, Deliverables, Deliverables, Deliverables, Objectives (+17 more)

### Community 3 - "Community 3"
Cohesion: 0.15
Nodes (15): Enum, build_frequent_contacts(), Deterministic graph edge generation. No LLM., upsert_person_topic(), driver(), init_constraints(), Neo4j driver wrapper., session() (+7 more)

### Community 4 - "Community 4"
Cohesion: 0.1
Nodes (19): 5.1 Scaffold, 5.2 API client, 5.3 Pages, 5.4 Graph view specifics, 5.5 Search UX, 5.6 Build & serve in production, code:python (from fastapi.middleware.cors import CORSMiddleware), code:block2 (FRONTEND_ORIGIN=http://localhost:5173) (+11 more)

### Community 5 - "Community 5"
Cohesion: 0.1
Nodes (19): Communities (9 total, 0 thin omitted), Community 0 - "Ingestion & Production", Community 1 - "LLM Reasoning & Intelligence", Community 2 - "MVP Foundation & Semantic Search", Community 3 - "Local Models & Memory Tiers", Community 4 - "Graph Intelligence (Neo4j)", Community 5 - "Core Principles & Vision", Community 6 - "Embedding & Retrieval" (+11 more)

### Community 6 - "Community 6"
Cohesion: 0.11
Nodes (18): 2.1 Bootstrap the Qdrant collection, 2.2 Embed-on-ingest, 2.3 Semantic search endpoint, 2.4 Backfill existing messages, 2.5 Search quality test, code:powershell (python -c "from embeddings.embedder import embed; embed(['wa), code:powershell (python -c "from embeddings.qdrant_store import ensure_collec), code:powershell (python -m scripts.backfill_embeddings) (+10 more)

### Community 7 - "Community 7"
Cohesion: 0.11
Nodes (18): 3.1 Initialize Neo4j constraints, 3.2 Entity extraction (deterministic, no LLM), 3.3 Edge generation pipeline, 3.4 FREQUENTLY_CONTACTS aggregation, 3.5 Graph query API, 3.6 Backfill graph from existing messages, code:powershell (python -c "from graph.neo4j_client import init_constraints; ), code:block2 (def index_message(msg: Message) -> None:) (+10 more)

### Community 8 - "Community 8"
Cohesion: 0.11
Nodes (18): 4.1 Priority scoring on ingest, 4.2 Priority Inbox endpoint, 4.3 Cluster-then-summarize daily digest, 4.4 Token budget enforcement, 4.5 Long-term memory tier rotation, 4.6 Behavioral analytics endpoint, 4.7 Scheduler bootstrap, code:block1 (all_messages_for_day  → embeddings already exist) (+10 more)

### Community 9 - "Community 9"
Cohesion: 0.11
Nodes (18): 6.1 Containerize the backend, 6.2 Encryption at rest, 6.3 Backups, 6.4 Observability, 6.5 Performance pass, 6.6 CI, 6.7 Documentation, code:python (from fastapi.staticfiles import StaticFiles) (+10 more)

### Community 10 - "Community 10"
Cohesion: 0.14
Nodes (9): AI budgeting (section 11). Gates LLM calls under a daily token budget., remaining(), TokenBudget, chat(), client(), Thin LM Studio wrapper. LM Studio exposes an OpenAI-compatible API., Daily/weekly summarization. Cluster-first, then LLM., summarize_clusters() (+1 more)

### Community 11 - "Community 11"
Cohesion: 0.12
Nodes (16): 1. Prerequisites, 2. Python virtualenv, 3. spaCy model (P3), 4. LM Studio, 5. Docker services (Qdrant, Neo4j), 6. Environment variables, 7. Smoke test, 8. Troubleshooting (+8 more)

### Community 12 - "Community 12"
Cohesion: 0.12
Nodes (16): 1.1 Persist the schema, 1.2 Wire the WhatsApp ingest endpoint, 1.3 Daily summary endpoint, 1.4 Logging, 1.5 Smoke-test the LLM path, code:powershell (. .\.venv\Scripts\Activate.ps1), code:python (from ai.lm_studio_client import chat), Configuration changes (+8 more)

### Community 13 - "Community 13"
Cohesion: 0.16
Nodes (10): Settings, add_request_id(), Base, BaseSettings, DailySummary, Message, Base, DeclarativeBase (+2 more)

### Community 14 - "Community 14"
Cohesion: 0.17
Nodes (16): Epic: Relationship Graph, Final Product Vision, Graph-Driven Contextual Understanding, Graph Schema, 100% Local Execution, Local-Only Security, Neo4j, Node: Emotion (+8 more)

### Community 15 - "Community 15"
Cohesion: 0.18
Nodes (9): ingest_whatsapp(), make_id(), Normalize parser output to the unified Message entity (section 12)., to_message_dict(), parse(), _parse_ts(), ParsedMessage, Deterministic WhatsApp TXT export parser. No LLM. (+1 more)

### Community 16 - "Community 16"
Cohesion: 0.23
Nodes (7): detect_urgency(), Lightweight NLP layer (section 6). spaCy + regex, no LLM., project_weight(), Deterministic priority scoring engine (section 14)., recency_weight(), score(), sender_weight()

### Community 17 - "Community 17"
Cohesion: 0.17
Nodes (11): 1. Vision, 21. Repository Structure, 22. MVP Scope Recommendation, 25. Final Product Vision, 3. LLM Usage Philosophy, 6. High-Level Architecture, code:text (┌───────────────────────┐), code:text (project-root/) (+3 more)

### Community 18 - "Community 18"
Cohesion: 0.22
Nodes (9): 13. Graph Schema, code:text (Person -> DISCUSSED -> Topic), Edge Types, Emotion, Event, Node Types, Person, Task (+1 more)

### Community 19 - "Community 19"
Cohesion: 0.25
Nodes (8): 8. Storage Architecture, Graph Database, Neo4j, PostgreSQL (Future Production), Qdrant, Relational Database, SQLite (Initial), Vector Database

### Community 20 - "Community 20"
Cohesion: 0.29
Nodes (6): 14. Priority Scoring Engine, Formula, Priority Signals, Project Relevance, Relationship Strength, Urgency Keywords

### Community 21 - "Community 21"
Cohesion: 0.29
Nodes (6): Architectural invariants (every phase must respect), Cross-phase milestones, Decision log, Reading order, Scope discipline, WaterwallAI — Master Execution Plan

### Community 22 - "Community 22"
Cohesion: 0.53
Nodes (5): client(), ensure_collection(), Qdrant client wrapper for semantic retrieval., search(), upsert()

### Community 24 - "Community 24"
Cohesion: 0.33
Nodes (6): 4. System Task Distribution, Infrastructure Tasks, Parsing and Ingestion, Recommended Technologies, System Intelligence, Tasks That MUST NOT Use the LLM

### Community 25 - "Community 25"
Cohesion: 0.33
Nodes (6): 7. Recommended Technology Stack, AI Runtime, Backend, Embedding Models, Fast Reasoning Models, Small Local Models

### Community 26 - "Community 26"
Cohesion: 0.4
Nodes (5): 23. Recommended Development Progression, Stage 1, Stage 2, Stage 3, Stage 4

### Community 28 - "Community 28"
Cohesion: 0.67
Nodes (3): embed(), _model(), Local embedding generation (section 7). Dedicated model, NOT the chat LLM.

### Community 29 - "Community 29"
Cohesion: 0.5
Nodes (4): 9. Multi-Tier Memory Architecture, Cold Memory, Hot Memory, Warm Memory

### Community 30 - "Community 30"
Cohesion: 0.5
Nodes (4): 17. Security Architecture, Authentication, Encryption, Local-Only Security

### Community 31 - "Community 31"
Cohesion: 0.5
Nodes (4): 11. AI Budgeting System, code:python (DAILY_LLM_TOKEN_BUDGET = 50000), Example Configuration, Optimization Rules

### Community 33 - "Community 33"
Cohesion: 0.67
Nodes (3): 5. Tasks That SHOULD Use the LLM, Recommended Flow, Semantic Reasoning

### Community 34 - "Community 34"
Cohesion: 0.67
Nodes (3): 12. Data Model, code:json ({), Message Entity

### Community 35 - "Community 35"
Cohesion: 0.67
Nodes (3): 20. Observability, Logging, Metrics

### Community 36 - "Community 36"
Cohesion: 0.67
Nodes (3): 2. Core Product Principles, Important Constraint, Primary Principles

### Community 37 - "Community 37"
Cohesion: 0.67
Nodes (3): 24. Success Metrics, Technical, User Metrics

### Community 38 - "Community 38"
Cohesion: 0.67
Nodes (3): 10. Task Orchestrator Architecture, code:text (New Message), Pipeline Example

### Community 39 - "Community 39"
Cohesion: 0.67
Nodes (3): 18. Performance Optimization Strategy, Main Bottlenecks, Optimizations

### Community 40 - "Community 40"
Cohesion: 0.67
Nodes (3): 19. Production Deployment, code:text (frontend), Docker Services

## Knowledge Gaps
- **235 isolated node(s):** `AI budgeting (section 11). Gates LLM calls under a daily token budget.`, `Thin LM Studio wrapper. LM Studio exposes an OpenAI-compatible API.`, `Daily/weekly summarization. Cluster-first, then LLM.`, `Local embedding generation (section 7). Dedicated model, NOT the chat LLM.`, `Qdrant client wrapper for semantic retrieval.` (+230 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `16. Phase-Wise Execution Plan` connect `Community 2` to `Community 17`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Why does `15. User Stories` connect `Community 1` to `Community 17`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **What connects `AI budgeting (section 11). Gates LLM calls under a daily token budget.`, `Thin LM Studio wrapper. LM Studio exposes an OpenAI-compatible API.`, `Daily/weekly summarization. Cluster-first, then LLM.` to the rest of the system?**
  _235 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.05 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.08 - nodes in this community are weakly interconnected._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.08 - nodes in this community are weakly interconnected._
- **Should `Community 4` be split into smaller, more focused modules?**
  _Cohesion score 0.1 - nodes in this community are weakly interconnected._
# Graph Report - .graphify_input  (2026-05-08)

## Corpus Check
- Corpus is ~1,960 words - fits in a single context window. You may not need a graph.

## Summary
- 77 nodes · 115 edges · 9 communities
- Extraction: 71% EXTRACTED · 29% INFERRED · 0% AMBIGUOUS · INFERRED: 33 edges (avg confidence: 0.86)
- Token cost: 45,000 input · 5,421 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Ingestion & Production|Ingestion & Production]]
- [[_COMMUNITY_LLM Reasoning & Intelligence|LLM Reasoning & Intelligence]]
- [[_COMMUNITY_MVP Foundation & Semantic Search|MVP Foundation & Semantic Search]]
- [[_COMMUNITY_Local Models & Memory Tiers|Local Models & Memory Tiers]]
- [[_COMMUNITY_Graph Intelligence (Neo4j)|Graph Intelligence (Neo4j)]]
- [[_COMMUNITY_Core Principles & Vision|Core Principles & Vision]]
- [[_COMMUNITY_Embedding & Retrieval|Embedding & Retrieval]]
- [[_COMMUNITY_Backend Stack|Backend Stack]]
- [[_COMMUNITY_Relational Storage|Relational Storage]]

## God Nodes (most connected - your core abstractions)
1. `Embedding Layer` - 11 edges
2. `AI Reasoning Layer` - 8 edges
3. `Graph Schema` - 8 edges
4. `Storage Layer` - 7 edges
5. `Backend Stack` - 7 edges
6. `PHASE 1 â€” Foundation` - 7 edges
7. `Docker Production Deployment` - 7 edges
8. `Ingestion Layer` - 6 edges
9. `PHASE 4 â€” Intelligence Engine` - 6 edges
10. `Smaller Local Models Constraint` - 6 edges

## Surprising Connections (you probably didn't know these)
- `Graph-Driven Contextual Understanding` --rationale_for--> `Graph Schema`  [INFERRED]
  local_ai_context_graph_system_production_blueprint.md → local_ai_context_graph_system_production_blueprint.md  _Bridges community 5 → community 4_
- `Priority Scoring Engine` --shares_data_with--> `Lightweight NLP Layer`  [INFERRED]
  local_ai_context_graph_system_production_blueprint.md → local_ai_context_graph_system_production_blueprint.md  _Bridges community 0 → community 1_
- `Message Entity (Data Model)` --shares_data_with--> `Priority Scoring Engine`  [INFERRED]
  local_ai_context_graph_system_production_blueprint.md → local_ai_context_graph_system_production_blueprint.md  _Bridges community 8 → community 1_
- `Epic: Semantic Search` --semantically_similar_to--> `Epic: Long-Term Memory`  [INFERRED] [semantically similar]
  local_ai_context_graph_system_production_blueprint.md → local_ai_context_graph_system_production_blueprint.md  _Bridges community 2 → community 1_
- `Lightweight NLP Layer` --shares_data_with--> `Embedding Layer`  [EXTRACTED]
  local_ai_context_graph_system_production_blueprint.md → local_ai_context_graph_system_production_blueprint.md  _Bridges community 0 → community 6_

## Hyperedges (group relationships)
- **Data Sources participating in Ingestion** — blueprint_whatsapp, blueprint_email, blueprint_notes, blueprint_docs_pdfs, blueprint_ingestion_layer [EXTRACTED 1.00]
- **Storage Architecture Backends** — blueprint_sqlite, blueprint_qdrant, blueprint_neo4j, blueprint_storage_layer [EXTRACTED 1.00]
- **Phase-Wise Execution Plan** — blueprint_phase_1, blueprint_phase_2, blueprint_phase_3, blueprint_phase_4, blueprint_phase_5, blueprint_phase_6 [EXTRACTED 1.00]

## Communities (9 total, 0 thin omitted)

### Community 0 - "Ingestion & Production"
Cohesion: 0.16
Nodes (15): Data Sources, Docker Production Deployment, Docs/PDFs, Email, Event-Driven Architecture, Frontend, Ingestion Layer, Lightweight NLP Layer (+7 more)

### Community 1 - "LLM Reasoning & Intelligence"
Cohesion: 0.24
Nodes (10): Epic: Behavioral Analytics, Epic: Daily Summary, Epic: Long-Term Memory, Epic: Priority Inbox, LLM Usage Philosophy, Tasks That SHOULD Use the LLM, Minimal LLM Dependency, Tasks That MUST NOT Use the LLM (+2 more)

### Community 2 - "MVP Foundation & Semantic Search"
Cohesion: 0.24
Nodes (10): Deterministic Pipelines, Recommended Development Progression, Epic: Chat Parsing, Epic: Semantic Search, FastAPI, MVP Scope Recommendation, PHASE 1 â€” Foundation, PHASE 2 â€” Semantic Layer (+2 more)

### Community 3 - "Local Models & Memory Tiers"
Cohesion: 0.2
Nodes (10): AI Budgeting System, AI Reasoning Layer, Cold Memory, Gemma 3B, Hot Memory, LM Studio, Ollama (Optional), Phi-3 Mini (+2 more)

### Community 4 - "Graph Intelligence (Neo4j)"
Cohesion: 0.33
Nodes (9): Epic: Relationship Graph, Graph Schema, Neo4j, Node: Emotion, Node: Event, Node: Person, Node: Task, Node: Topic (+1 more)

### Community 5 - "Core Principles & Vision"
Cohesion: 0.38
Nodes (7): Final Product Vision, Graph-Driven Contextual Understanding, 100% Local Execution, Local-Only Security, Persistent Contextual Memory, Privacy-First Architecture, Vision: Local-First AI Memory OS

### Community 6 - "Embedding & Retrieval"
Cohesion: 0.29
Nodes (7): BGE-small, Embedding Layer, all-MiniLM-L6-v2, nomic-embed-text, Performance Optimization Strategy, Retrieval-First Intelligence, Success Metrics

### Community 7 - "Backend Stack"
Cohesion: 0.4
Nodes (5): APScheduler, AsyncIO, Backend Stack, Python, SQLAlchemy

### Community 8 - "Relational Storage"
Cohesion: 0.67
Nodes (4): Message Entity (Data Model), PostgreSQL (Future Production), SQLite (Initial), Storage Layer

## Knowledge Gaps
- **23 isolated node(s):** `Retrieval-First Intelligence`, `Event-Driven Architecture`, `Deterministic Pipelines`, `WhatsApp`, `Email` (+18 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `AI Reasoning Layer` connect `Local Models & Memory Tiers` to `Relational Storage`, `Ingestion & Production`, `Embedding & Retrieval`?**
  _High betweenness centrality (0.197) - this node is a cross-community bridge._
- **Why does `Graph Schema` connect `Graph Intelligence (Neo4j)` to `Core Principles & Vision`?**
  _High betweenness centrality (0.186) - this node is a cross-community bridge._
- **Why does `Embedding Layer` connect `Embedding & Retrieval` to `Ingestion & Production`, `Relational Storage`, `MVP Foundation & Semantic Search`?**
  _High betweenness centrality (0.182) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `Graph Schema` (e.g. with `Graph-Driven Contextual Understanding` and `Neo4j`) actually correct?**
  _`Graph Schema` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Retrieval-First Intelligence`, `Event-Driven Architecture`, `Deterministic Pipelines` to the rest of the system?**
  _23 weakly-connected nodes found - possible documentation gaps or missing edges._
# WaterwallAI — Master Execution Plan

This is the index of phase-by-phase execution plans for building WaterwallAI per the [blueprint](../local_ai_context_graph_system_production_blueprint.md).

## Reading order

1. [CONFIGURATION.md](CONFIGURATION.md) — one-time host setup (Python, Docker, LM Studio, env vars). **Do this first.**
2. [PLAN_PHASE_01_FOUNDATION.md](PLAN_PHASE_01_FOUNDATION.md) — FastAPI + SQLite + WhatsApp ingestion + LM Studio smoke test
3. [PLAN_PHASE_02_SEMANTIC.md](PLAN_PHASE_02_SEMANTIC.md) — embeddings + Qdrant + semantic search
4. [PLAN_PHASE_03_GRAPH.md](PLAN_PHASE_03_GRAPH.md) — Neo4j + entity extraction + edge builders
5. [PLAN_PHASE_04_INTELLIGENCE.md](PLAN_PHASE_04_INTELLIGENCE.md) — priority engine + scheduled summaries + budgeting
6. [PLAN_PHASE_05_FRONTEND.md](PLAN_PHASE_05_FRONTEND.md) — React UI (dashboard, graph, timeline, search)
7. [PLAN_PHASE_06_HARDENING.md](PLAN_PHASE_06_HARDENING.md) — Docker compose, encryption, monitoring, backups

## Architectural invariants (every phase must respect)

These come from the blueprint and are **load-bearing**. Violating them produces a slow or unprivate system:

1. **No cloud calls.** All inference is local (LM Studio) or deterministic Python.
2. **LLM is the last resort.** Default to rules / regex / spaCy / vector search / graph traversal. Only call the LLM when semantic reasoning is genuinely required (blueprint §3, §5).
3. **Embeddings come from a dedicated embedding model**, NOT the chat LLM (blueprint §7).
4. **Hot/Warm/Cold memory tiers.** Only Hot enters the LLM context window (blueprint §9).
5. **Token budget gates every LLM call.** See [ai/budget.py](../ai/budget.py).
6. **Pipelines are deterministic event chains, not agentic loops** (blueprint §10).

## Cross-phase milestones

| Milestone | Earliest phase | Definition of "done" |
|---|---|---|
| First parsed message in DB | P1 | `/ingest/whatsapp` returns 200 and a row exists in SQLite |
| First LLM-generated summary | P1 | `/summary/daily` returns non-empty text from a small Qwen/Phi model |
| First semantic-search hit | P2 | `/search` returns the correct message for a paraphrased query |
| First graph traversal | P3 | Cypher query returns frequent contacts / topic clusters |
| First scheduled digest | P4 | APScheduler runs at 07:00 and persists a summary row |
| First end-to-end UI flow | P5 | Browser → search box → results render with snippets |
| Production-ready deploy | P6 | `docker compose up` brings up all services with encrypted DB and backup script |

## Decision log

Track non-obvious decisions in `docs/DECISIONS.md` as you go. Examples worth recording:
- Which embedding model you settled on and why
- LM Studio model choice + observed tokens/sec
- spaCy model size (sm vs md vs lg)
- Any deviation from the blueprint and the reason

## Scope discipline

Per blueprint §22, the **MVP is**: WhatsApp ingestion + SQLite + embeddings + semantic search + daily summaries + basic graph view. Anything else (multi-agent, autonomous planning, recursive memory, voice) is post-MVP and should not be implemented during P1–P3.

# Phase 4 — Intelligence Engine

**Duration:** 3 weeks. **Blueprint reference:** §10 Task Orchestrator, §11 AI Budgeting, §14 Priority Scoring, §15 Epic Priority Inbox / Long-Term Memory / Behavioral Analytics.

## Goal

End of phase: the system runs **on its own** — daily digests appear at 07:00, priority scores rank an inbox, the LLM never blows the token budget, and the user gets behavioral analytics over time.

## Pre-requisites

- Phases 1–3 complete (ingestion, embeddings, graph all live)
- A few weeks of real messages ingested so analytics has signal

## Configuration changes

| Var | Tune to your model |
|---|---|
| `DAILY_LLM_TOKEN_BUDGET` | start 50_000, raise if you upgrade beyond 3B |
| `MAX_CONTEXT_MESSAGES` | 25 is conservative; small models lose coherence above ~40 |
| `SUMMARY_BATCH_SIZE` | 50 means we summarize per 50-message cluster |
| `LLM_PRIORITY_THRESHOLD` | 0.7 — messages above this trigger LLM enrichment |

Add a new var: `ACTIVE_PROJECT_TERMS` (comma-separated lowercase keywords) — feeds `nlp.priority.score`. Also add a `frequent_contacts` cache populated from Neo4j once a day so the priority engine doesn't hit Neo4j per-message.

## Execution steps

### 4.1 Priority scoring on ingest

[nlp/priority.py](../nlp/priority.py) is implemented. Wire it into the ingest pipeline:

1. Maintain a lazily-loaded `frequent_contacts: set[str]` cache populated from `MATCH (a)-[:FREQUENTLY_CONTACTS]-(b) RETURN a.name`.
2. Maintain `active_project_terms: set[str]` from the env var.
3. Per message: `score = nlp.priority.score(body, ts, sender, frequent_contacts, active_project_terms)` → write into `Message.priority_score`.
4. Both caches refresh on a 1-hour interval via APScheduler.

### 4.2 Priority Inbox endpoint

`GET /inbox?since=...&min_score=0.6&limit=50` in `backend/app/api/inbox.py`:
- SQL `WHERE priority_score >= min_score AND timestamp >= since ORDER BY priority_score DESC, timestamp DESC LIMIT ...`
- Return id, sender, snippet, score, reasons (which weights contributed most — handy for UI debugging)

### 4.3 Cluster-then-summarize daily digest

This is the **core LLM-budget pattern** (blueprint §5):

```
all_messages_for_day  → embeddings already exist
                       ↓
                cluster by cosine similarity (sklearn AgglomerativeClustering with distance threshold)
                       ↓
                for each cluster: pick top-3 messages by priority_score → "excerpt"
                       ↓
                ai.summarizer.summarize_clusters([excerpt for each cluster])
                       ↓
                persist to daily_summaries (replace P1's single-shot version)
```

Implement in `ai/digest.py`. Run from `scheduler.jobs.daily_digest_job` at 07:00 cron. The LLM call is gated by `ai.budget.budget` — if budget is gone, write a placeholder summary and queue retry for next day.

### 4.4 Token budget enforcement

[ai/budget.py](../ai/budget.py) is implemented. Hard-wire it in front of every `chat()` call site (currently only `summarizer`; will grow). Add a `/admin/budget` endpoint that returns `{used, remaining, daily_limit}` so you can spot bugs without grep'ing logs.

### 4.5 Long-term memory tier rotation

Per blueprint §9, three tiers:

| Tier | Where | What |
|---|---|---|
| Hot | SQLite + Qdrant + Neo4j | last 7 days, all enriched |
| Warm | Qdrant only (SQLite trimmed of body, summary kept) | days 8–90 |
| Cold | Compressed JSONL on disk + a single weekly summary | older than 90 days |

Implement `scheduler.jobs.tier_rotation_job` (nightly):
1. Find messages older than 7 days with no summary → cluster + summarize.
2. Strip raw body from SQLite (keep `summary`, `topics`, `entities`).
3. After 90 days → export to `data/cold/YYYY-MM.jsonl.gz`, delete from SQLite + Qdrant.

This is what keeps the system feasible on a laptop after a year of use. Don't skip it.

### 4.6 Behavioral analytics endpoint

`GET /analytics/communication?from=...&to=...`:
- Messages per day (line)
- Top 10 contacts by volume
- Top 10 topics by trend (count delta vs previous period)
- Most common urgency/sentiment per contact

All deterministic SQL/Cypher — no LLM.

### 4.7 Scheduler bootstrap

Update [backend/app/main.py](../backend/app/main.py) to start the scheduler on FastAPI startup (`@app.on_event("startup")`) and shut down cleanly. Use `scheduler.jobs.build_scheduler()`.

## User stories satisfied

- **Epic: Priority Inbox**
- **Epic: Long-Term Memory**
- **Epic: Behavioral Analytics**

## Tests

| Test | What it asserts |
|---|---|
| `tests/test_priority.py` | weights produce expected ordering for fixtures (urgent + frequent contact > old + stranger) |
| `tests/test_clustering.py` | semantically similar messages cluster together; dissimilar ones don't |
| `tests/test_budget.py` | budget rolls over at midnight; concurrent spend is thread-safe |
| `tests/test_tier_rotation.py` | a 100-day-old message ends up in cold storage and is removed from Qdrant |
| `tests/test_digest_e2e.py` | full pipeline on a fixture day produces a non-empty summary persisted in DB |

## Definition of done

- [ ] Daily digest runs unattended for 3 consecutive days without manual intervention
- [ ] Token budget never exceeds `DAILY_LLM_TOKEN_BUDGET` (verify from `/admin/budget` history)
- [ ] Priority Inbox reorders correctly when a known-frequent contact sends an "urgent" message
- [ ] Tier rotation job is observable (logs show counts moved Hot→Warm→Cold)
- [ ] Analytics endpoint returns data in <1s on a year of messages

## Watch-outs

- **Clustering thresholds depend on the embedding model.** MiniLM cosine ~0.7 is "same topic". Test on real data before trusting defaults.
- **Cron jobs and `--reload` don't mix.** Disable APScheduler when uvicorn is in reload mode, or you'll spawn duplicate jobs.
- **Budget reset uses local time.** If the user's machine sleeps through midnight, the rollover happens on next call. That's fine — just don't alert on stale `last_reset`.

## Out of scope

UI (P5), encryption / production hardening (P6).

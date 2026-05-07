# Phase 1 — Foundation

**Duration:** 2–3 weeks. **Blueprint reference:** §15 Epic Chat Parsing, §16 Phase 1, §22 MVP scope.

## Goal

End of phase: a user can POST a WhatsApp `.txt` export, the messages persist in SQLite, and `/summary/daily` returns an LLM-generated summary of one day's messages.

## Pre-requisites

- [CONFIGURATION.md](CONFIGURATION.md) complete (venv, LM Studio running, `.env` populated)
- Qdrant and Neo4j containers are NOT required for P1

## Configuration changes

None beyond P0 setup. P1 uses only SQLite + LM Studio.

## Execution steps

### 1.1 Persist the schema

Create the SQLite file and tables.

```powershell
. .\.venv\Scripts\Activate.ps1
python -c "from backend.app.db.session import engine, Base; from backend.app.db import models; Base.metadata.create_all(engine); print('schema created')"
```

The `Message` model already lives in [backend/app/db/models.py](../backend/app/db/models.py) and matches blueprint §12.

### 1.2 Wire the WhatsApp ingest endpoint

[ingestion/whatsapp_parser.py](../ingestion/whatsapp_parser.py) is already written and unit-tested. Wire it into [backend/app/api/ingest.py](../backend/app/api/ingest.py):

- Accept multipart upload of a `.txt` file
- Decode as UTF-8
- Iterate `parse(text)` from the parser
- For each `ParsedMessage`, build a row with `ingestion.normalizer.to_message_dict("whatsapp", sender, ts, body)`
- Insert via `SessionLocal()`; use `session.merge()` so re-uploads of the same export are idempotent (the deterministic id from `make_id` handles dedup)
- Return `{"inserted": int, "skipped": int}`

**Acceptance:** `pytest tests/test_whatsapp_parser.py` passes, plus a new `tests/test_ingest_endpoint.py` that POSTs the sample export and asserts row count.

### 1.3 Daily summary endpoint

In [backend/app/api/summary.py](../backend/app/api/summary.py):

- `/summary/daily?date=YYYY-MM-DD` (default = today)
- Query `Message` rows for that day, ordered by timestamp
- If 0 messages → `{"summary": "", "messages": 0}`
- Otherwise build a single user-string of `[HH:MM] sender: body` lines, capped at `settings.max_context_messages` (drop the oldest if over)
- Call `ai.summarizer.summarize_clusters([excerpt])` — for P1 we pass one big excerpt; clustering arrives in P4
- Persist the result in a new `daily_summaries` table (date, body, model, generated_at) so re-requests are cached

**Acceptance:** with a small WhatsApp export ingested, `curl /summary/daily?date=...` returns text summarizing actual conversations, not boilerplate. Hitting the same date twice should return the cached row instantly (no second LM Studio call).

### 1.4 Logging

Wire structured logging at app startup in [backend/app/main.py](../backend/app/main.py):

- Use stdlib `logging.basicConfig(level=settings.log_level, format='%(asctime)s %(name)s %(levelname)s %(message)s')`
- Add request-id middleware (uuid4 per request) — useful when P4 scheduled jobs start writing logs concurrently

### 1.5 Smoke-test the LLM path

Add `scripts/smoke_lm_studio.py`:

```python
from ai.lm_studio_client import chat
print(chat("You are a terse assistant.", "Reply with exactly: PONG"))
```

Run it. If output isn't `PONG`, your model is wrong / not loaded / running cold. Fix before continuing — every later phase depends on this working.

## User stories satisfied

- **Epic: Chat Parsing** — Import TXT export, parse timestamps, detect senders, store messages
- **Epic: Daily Summary** — Summaries generated automatically (manual trigger here; cron arrives in P4)

## Tests to write

| Test | What it asserts |
|---|---|
| `tests/test_whatsapp_parser.py` | parser handles multi-line bodies, multiple date formats |
| `tests/test_ingest_endpoint.py` | round-trip: upload → row count → idempotency on re-upload |
| `tests/test_summary_cache.py` | second call to `/summary/daily` does not hit LM Studio |

Use `pytest` + `httpx.AsyncClient` for endpoint tests. Mock LM Studio via a fixture that monkey-patches `ai.lm_studio_client.chat`.

## Definition of done

- [ ] WhatsApp export round-trips through `/ingest/whatsapp` without data loss
- [ ] `/summary/daily` returns coherent text from local LLM
- [ ] Summary is cached per date; second call is sub-100ms
- [ ] All P1 tests green
- [ ] No external network calls (verify with `netstat` or by disabling Wi-Fi during test)

## Out of scope for P1

Embeddings, semantic search, Qdrant, Neo4j, priority scoring, scheduled jobs, frontend. Those start in P2.

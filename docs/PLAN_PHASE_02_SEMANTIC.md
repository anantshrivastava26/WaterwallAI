# Phase 2 — Semantic Layer

**Duration:** 2 weeks. **Blueprint reference:** §15 Epic Semantic Search, §16 Phase 2.

## Goal

End of phase: a user can ask "what did Alice say about the budget last month?" in natural language and get the most semantically relevant messages back, even when the query shares no words with the messages.

## Pre-requisites

- Phase 1 done (messages flowing into SQLite)
- Qdrant container running (see [CONFIGURATION.md](CONFIGURATION.md) §5)

## Configuration changes

| Var in [.env](../.env) | Notes |
|---|---|
| `EMBEDDING_MODEL` | confirm it's `sentence-transformers/all-MiniLM-L6-v2` (fast, 384-dim) — only change for a tested reason |
| `EMBEDDING_DIM` | 384 for MiniLM; 768 for nomic-embed-text. **Must match `EMBEDDING_MODEL`** |
| `QDRANT_COLLECTION` | leave default; if you ever change the embedding model, change the collection name too so dimensions don't collide |

First run of `embeddings.embedder.embed` downloads the model (~80MB) into `~/.cache/huggingface`. Pre-warm it during setup:

```powershell
python -c "from embeddings.embedder import embed; embed(['warmup'])"
```

## Execution steps

### 2.1 Bootstrap the Qdrant collection

```powershell
python -c "from embeddings.qdrant_store import ensure_collection; ensure_collection(); print('ok')"
```

[embeddings/qdrant_store.py](../embeddings/qdrant_store.py) creates the collection idempotently with cosine distance and the configured dimension.

### 2.2 Embed-on-ingest

Modify the ingest pipeline so every newly-inserted `Message` produces a vector:

1. After SQLite insert in [backend/app/api/ingest.py](../backend/app/api/ingest.py), batch the new bodies into `embeddings.embedder.embed(bodies)`.
2. Upsert into Qdrant with `embeddings.qdrant_store.upsert(ids, vectors, payloads)`. Payload should include `{sender, timestamp_iso, source}` so retrieval can filter without a SQLite roundtrip.
3. Set `Message.embedding_id = id` (same id we used in SQLite — keeps lookups simple).
4. Batch size = 64. Embedding is the bottleneck; never embed one-at-a-time.

### 2.3 Semantic search endpoint

In [backend/app/api/search.py](../backend/app/api/search.py):

- Accept `{query: str, top_k: int = 10, since: date | null, sender: str | null}`
- Embed the query (single-string call to `embed`)
- Call `qdrant_store.search(vector, top_k=top_k * 3)` — overshoot, then filter
- Apply `since` / `sender` filters from the payload (cheap; no SQLite hit unless rendering)
- Hydrate the top `top_k` survivors from SQLite for full body + metadata
- Return `[{id, score, sender, timestamp, snippet}]`

**Snippet** = first 240 chars of body. Don't return the full message in search results — frontend asks for it on click.

### 2.4 Backfill existing messages

If P1 ingested messages before embeddings existed, write a one-shot:

```powershell
python -m scripts.backfill_embeddings
```

`scripts/backfill_embeddings.py` should:
- Select all `Message` rows where `embedding_id IS NULL`
- Iterate in batches of 64
- Embed + upsert + update SQLite

Make it resumable (commit every batch) so a crash doesn't restart from zero.

### 2.5 Search quality test

Build `tests/test_search_quality.py` with a fixed corpus of ~30 hand-crafted messages and a list of (query, expected_top_message_id) pairs. Assert the expected message lands in `top_3` for each query. This is the regression test for any future embedding-model swap.

## User stories satisfied

- **Epic: Semantic Search** — Natural-language search, vector retrieval, similar-message grouping

## Tests

| Test | What it asserts |
|---|---|
| `tests/test_embeddings.py` | embed returns vectors of `EMBEDDING_DIM`; same input → same vector (deterministic) |
| `tests/test_qdrant_roundtrip.py` | upsert + search returns the inserted id with score > 0.9 |
| `tests/test_search_quality.py` | paraphrased queries find their target messages |

Mark Qdrant tests `@pytest.mark.integration` and skip when `QDRANT_URL` is unreachable, so CI on a laptop without Docker still passes the unit tier.

## Definition of done

- [ ] Every message in SQLite has a non-null `embedding_id` and a Qdrant point
- [ ] `/search` returns results in <300ms for top_k=10 on a corpus of 10k messages
- [ ] Paraphrase-quality test green
- [ ] Backfill script is idempotent (running it twice does not duplicate Qdrant points)
- [ ] No degradation in P1 endpoints

## Out of scope

Graph relationships, priority scoring, scheduled re-embedding, multi-language embeddings.

## Watch-outs

- **Dimension mismatch on model swap.** Always change `QDRANT_COLLECTION` when you change `EMBEDDING_MODEL`, or drop the old collection first.
- **Don't embed during request handling synchronously for large uploads.** A 50k-message export at 64 msgs/batch on CPU is ~2 minutes. Either return 202 + background task, or embed in a worker. For P2 keep it synchronous and document the limit; move to background in P4.

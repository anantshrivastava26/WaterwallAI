# Phase 6 — Production Hardening

**Duration:** 2 weeks. **Blueprint reference:** §17 Security, §18 Performance, §19 Deployment, §20 Observability.

## Goal

End of phase: a single command (`docker compose up -d`) brings up the whole system on a fresh machine with: encrypted DB at rest, automated backups, structured logs, basic metrics, and a tested restore procedure.

## Pre-requisites

- All of P1–P5 done and stable
- `frontend/dist/` exists (run `npm run build` before starting P6)

## Scope: what this phase is NOT

It is **not** about hardening for the public internet. WaterwallAI is local-first; the threat model is:

1. Laptop theft / disk dump → covered by encryption at rest.
2. Crash / data corruption → covered by backups.
3. Bug in our code that wedges a service → covered by health checks + restart.

No multi-user auth, no JWT issuance, no rate limiting, no public TLS. If you decide later to expose this, that's a different phase entirely.

## Execution steps

### 6.1 Containerize the backend

[docker/Dockerfile.backend](../docker/Dockerfile.backend) is already in place. Improve it:

- Multi-stage build: stage 1 installs deps, stage 2 copies `.venv` + app
- Non-root user (`USER appuser`)
- `HEALTHCHECK CMD curl -f http://localhost:8000/health || exit 1`

Update [docker/docker-compose.yml](../docker/docker-compose.yml):
- Add `restart: unless-stopped` to all services
- Add `healthcheck` blocks
- Pin all image tags to specific patch versions (no `:latest`)
- Mount `frontend/dist` into the backend container at `/app/frontend/dist`

Wire static serving in [backend/app/main.py](../backend/app/main.py):
```python
from fastapi.staticfiles import StaticFiles
app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="frontend")
```
Mount this **last** so API routes win.

### 6.2 Encryption at rest

**SQLite:** swap `sqlite3` for `sqlcipher3-binary`. Update `Settings`:
- `SQLITE_PASSPHRASE` (read from OS keyring on Linux/macOS, DPAPI on Windows; fallback to env var with a warning)
- Connection string: `sqlite+pysqlcipher://:passphrase@//path/to/db?cipher=aes-256-cfb&kdf_iter=64000`

**Qdrant:** no built-in encryption. Mount its `qdrant_storage` volume on an encrypted filesystem (BitLocker on Windows, LUKS on Linux, FileVault on macOS). Document this — don't try to encrypt at app layer.

**Neo4j:** Community edition has no encryption at rest. Same approach — encrypted host filesystem.

Document the threat-model gap honestly: "Vector and graph stores rely on host-level disk encryption; do not run on an unencrypted disk."

### 6.3 Backups

Add `scripts/backup.ps1`:

```powershell
$ts = Get-Date -Format "yyyyMMdd-HHmmss"
$out = "backups/$ts"
New-Item -ItemType Directory -Force -Path $out | Out-Null

# SQLite — use VACUUM INTO for online backup
python -c "import sqlite3; sqlite3.connect('data/waterwall.sqlite').execute(\"VACUUM INTO 'backups/$ts/waterwall.sqlite'\")"

# Qdrant — snapshot API
curl -X POST http://localhost:6333/collections/waterwall_messages/snapshots
# fetch the snapshot file path from response, copy to $out

# Neo4j — neo4j-admin dump
docker compose exec neo4j neo4j-admin database dump neo4j --to-path=/var/lib/neo4j/backups
docker cp $(docker compose ps -q neo4j):/var/lib/neo4j/backups $out/

# Compress
Compress-Archive -Path $out\* -DestinationPath "$out.zip"
Remove-Item -Recurse $out
```

Schedule weekly via APScheduler. Keep last 8 backups, prune older.

Add `scripts/restore.ps1` and **rehearse it once**. An untested backup is a wish.

### 6.4 Observability

**Logs:** structured JSON via `python-json-logger`. One handler, rotating file at `logs/app.log`, max 10MB × 5 files. Stdout in dev, file in prod (toggle via `LOG_HANDLER` env).

**Metrics:** Prometheus client exposed at `/metrics`:
- `ingest_messages_total`
- `embedding_seconds` (histogram)
- `llm_request_seconds` (histogram, label by model)
- `llm_tokens_used_total` (counter)
- `qdrant_search_seconds`
- `priority_score` (histogram, sample 1%)

If the user runs Grafana, document a starter dashboard JSON in `docs/grafana_dashboard.json`. If not, `/metrics` is still useful via curl.

**Traces:** skip OpenTelemetry. Overkill for a single-user system.

### 6.5 Performance pass

Re-read blueprint §18 and confirm:
- [ ] Embeddings batched everywhere (no per-message embed calls)
- [ ] Summaries cached by date+message_set hash
- [ ] Graph queries use indexes (the constraints in [graph/schema.py](../graph/schema.py) provide them)
- [ ] Lazy graph loading on the frontend
- [ ] Streaming retrieval for large search results (use FastAPI `StreamingResponse` if you ever return >100 results)

Run `scripts/load_test.py` (write it): ingest 50k messages, then run 100 random searches. Report p50/p95 latency. Set a regression bar in CI.

### 6.6 CI

Minimal GitHub Actions / local pre-commit:

- `ruff check .`
- `pytest -m "not integration"` for unit
- Optional: integration tests against ephemeral docker compose

Don't push artifacts anywhere — local-first.

### 6.7 Documentation

Update `docs/`:
- `OPERATIONS.md` — how to start, stop, restart, backup, restore, view logs, view metrics
- `THREAT_MODEL.md` — what we protect against, what we don't, host requirements
- `RUNBOOK.md` — symptom → likely cause → fix table for the top 10 failure modes

## Tests

- Backup/restore round-trip test: dump → wipe data dir → restore → verify message count + a sample search still works
- Healthcheck: kill backend container, verify Docker restarts it within 30s
- Encryption: open `waterwall.sqlite` with plain `sqlite3` and confirm it errors

## Definition of done

- [ ] Fresh machine: clone → `docker compose up -d` → working app at http://localhost:8000
- [ ] Backups produced weekly, restore rehearsed
- [ ] No plaintext data leaves the host (verify with packet capture during ingest)
- [ ] `/metrics` returns counters and histograms
- [ ] `RUNBOOK.md` exists and the team has read it

## Watch-outs

- **sqlcipher build issues on Windows.** If pip wheel doesn't exist for your Python, fall back to host-disk encryption (BitLocker) and document it.
- **Backup of an in-flight Qdrant write.** Use the snapshot API, not raw file copy.
- **Don't `latest`-tag.** A silent minor-version Neo4j bump can break Cypher queries you depend on.

## Out of scope

Multi-user auth, biometric unlock (blueprint mentions it as "future"), cloud sync, mobile clients.

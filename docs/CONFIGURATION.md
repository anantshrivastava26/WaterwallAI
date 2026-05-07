# Configuration & Host Setup

One-time setup of the developer host. Do this before Phase 1.

## 1. Prerequisites

| Component | Min version | Why |
|---|---|---|
| Python | 3.12 | typed dict syntax, sqlalchemy 2.x |
| Docker Desktop | 4.x | runs Qdrant + Neo4j |
| LM Studio | 0.3+ | local OpenAI-compatible LLM server |
| Git | any | obvious |
| Node.js | 20 LTS | only needed in P5 (frontend) |

Windows users: PowerShell 7+ recommended. The `scripts/*.ps1` helpers assume `pwsh`.

## 2. Python virtualenv

```powershell
.\scripts\setup.ps1
```

That script creates `.venv`, installs [requirements.txt](../requirements.txt), copies `.env.example` to `.env` if missing, and creates `data/`.

After it finishes, every shell session must activate the venv:

```powershell
. .\.venv\Scripts\Activate.ps1
```

## 3. spaCy model (P3)

```powershell
python -m spacy download en_core_web_sm
```

Use `en_core_web_md` only if you need word vectors — we don't (vectors come from sentence-transformers).

## 4. LM Studio

1. Install LM Studio.
2. **Models tab** → search and download **one** chat model:
   - `qwen2.5-3b-instruct` (recommended — fast, decent reasoning)
   - or `phi-3-mini-4k-instruct`
   - or `gemma-2-2b-it`
3. **Developer tab** → **Start Server** (default port `1234`).
4. Load the chat model from the dropdown in the server panel.
5. Copy the model identifier shown in the server log into [.env](../.env) as `LM_STUDIO_MODEL`.

**Do not** load an embedding model in LM Studio — embeddings are generated locally by `sentence-transformers` (blueprint §7). Mixing the two wastes VRAM.

### Verify

```powershell
curl http://localhost:1234/v1/models
```

Should return a JSON list including the model you loaded.

## 5. Docker services (Qdrant, Neo4j)

```powershell
docker compose -f docker/docker-compose.yml up -d qdrant neo4j
```

Wait ~30s on first run for Neo4j to provision. Verify:

| Service | URL | Expected |
|---|---|---|
| Qdrant | http://localhost:6333/dashboard | dashboard loads |
| Neo4j | http://localhost:7474 | login screen — user `neo4j`, password from [.env](../.env) |

The backend container is started later in P6; for P1–P5 you run uvicorn directly against the host.

## 6. Environment variables

Edit [.env](../.env). The only value you almost certainly need to change is `LM_STUDIO_MODEL` (must match what LM Studio reports). Everything else has a working default.

| Var | Purpose | When to change |
|---|---|---|
| `LM_STUDIO_MODEL` | which chat model to call | always — set to your loaded model |
| `LM_STUDIO_BASE_URL` | LM Studio endpoint | only if you ran LM Studio on a non-default port |
| `EMBEDDING_MODEL` | sentence-transformers model id | if you swap to BGE or nomic |
| `EMBEDDING_DIM` | vector dimension | **must match** the embedding model (MiniLM=384, BGE-small=384, nomic-embed-text=768) |
| `NEO4J_PASSWORD` | graph DB auth | change before any deploy beyond localhost |
| `DAILY_LLM_TOKEN_BUDGET` | gate on LLM spend | raise when running on a beefier model |

## 7. Smoke test

After setup, this should succeed:

```powershell
. .\.venv\Scripts\Activate.ps1
python -c "from backend.app.config import settings; print(settings.lm_studio_base_url, settings.embedding_model)"
uvicorn backend.app.main:app --reload
# in another shell:
curl http://localhost:8000/health
```

Expected: `{"status":"ok"}`.

## 8. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `OpenAI returned 404 model not found` | `LM_STUDIO_MODEL` doesn't match loaded model | copy exact id from LM Studio server log |
| `Connection refused 1234` | server not started in LM Studio | Developer tab → Start Server |
| Qdrant `400 wrong vector size` | `EMBEDDING_DIM` mismatch | drop collection, fix env, restart |
| Neo4j auth error | password mismatch with volume | `docker compose down -v` to reset (destroys data) |
| Slow embeddings | first run downloads the model | wait once; cached in `~/.cache/huggingface` |

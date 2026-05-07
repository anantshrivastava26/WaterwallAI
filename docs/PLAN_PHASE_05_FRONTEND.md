# Phase 5 — Frontend UX

**Duration:** 3 weeks. **Blueprint reference:** §6 Frontend layer, §16 Phase 5.

## Goal

End of phase: a single-page React app at `http://localhost:5173` that exposes:
1. **Dashboard** — today's digest, priority inbox, top contacts/topics
2. **Graph view** — interactive force-directed view of the Neo4j graph
3. **Timeline** — chronological message scroll, jump-by-date
4. **Semantic Search** — natural-language input, ranked results with snippets

## Pre-requisites

- Phases 1–4 complete; APIs return real data
- Node 20 LTS + pnpm or npm

## Configuration changes

Add a CORS origin for the Vite dev server in [backend/app/main.py](../backend/app/main.py):

```python
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Add to [.env](../.env):
```
FRONTEND_ORIGIN=http://localhost:5173
```
Read it in `Settings`; never hardcode.

## Tech choices

| Concern | Choice | Why |
|---|---|---|
| Framework | React 18 + Vite + TypeScript | fast dev loop, no SSR needed (local app) |
| Routing | React Router 6 | minimal |
| State | TanStack Query | caches API responses; perfect for read-heavy local app |
| UI kit | Tailwind + shadcn/ui | composable, no heavy framework lock-in |
| Graph viz | `react-force-graph` (2D) | works with Neo4j-shaped JSON; can swap to Sigma.js if perf needs |
| Charts | `recharts` | analytics endpoints |

If the user prefers a different stack later, the API contract is stable so swapping is local to `frontend/`.

## Execution steps

### 5.1 Scaffold

```powershell
cd frontend
npm create vite@latest . -- --template react-ts
npm install
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
npm install @tanstack/react-query react-router-dom react-force-graph-2d recharts axios
```

Add Tailwind's `content` config to scan `./src/**/*.{ts,tsx}`.

### 5.2 API client

`frontend/src/api/client.ts`:
- One axios instance with `baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'`
- Typed wrappers: `getDailySummary(date)`, `searchMessages(query, opts)`, `getInbox(opts)`, `getGraphPeople()`, `getGraphPath(from, to)`, `getAnalytics(range)`.
- One source of truth for types. Generate from FastAPI's OpenAPI schema if you want zero drift: `npx openapi-typescript http://localhost:8000/openapi.json -o src/api/types.ts`.

### 5.3 Pages

| Route | Component | API |
|---|---|---|
| `/` | `Dashboard` | `/summary/daily`, `/inbox`, `/graph/people?top=10` |
| `/search` | `SearchPage` | `/search` |
| `/graph` | `GraphPage` | `/graph/people`, `/graph/topics` |
| `/timeline` | `TimelinePage` | `/messages?date=...` (new endpoint, keep simple) |
| `/analytics` | `AnalyticsPage` | `/analytics/communication` |

Keep components dumb — fetch logic lives in `useQuery` hooks (`useDailySummary`, `useInbox`, etc.) under `src/hooks/`.

### 5.4 Graph view specifics

`react-force-graph-2d` wants `{nodes: [{id,label,group}], links: [{source,target,relation,weight}]}`. Add a backend endpoint `GET /graph/snapshot?max_nodes=200` that returns this exact shape so the frontend doesn't reshape.

- Color nodes by `group` = node label (`Person`, `Topic`, …)
- Edge thickness = `weight` (clamp 1–8)
- Click a node → side panel with full neighborhood (call `/graph/person/{name}/topics` etc.)

### 5.5 Search UX

- Debounce input 300ms
- Show top_k=10 results with sender, timestamp, snippet
- Click a result → modal with full body + "Show in graph" link to `/graph?focus=...`

### 5.6 Build & serve in production

For P6 we serve the built bundle from FastAPI directly:

```powershell
cd frontend && npm run build
```

Output to `frontend/dist/`. P6 will mount it via `app.mount("/", StaticFiles(directory="frontend/dist", html=True))`.

## Tests

| Test | Tool |
|---|---|
| Component smoke tests for Dashboard / Search | Vitest + Testing Library |
| API mock layer | MSW (Mock Service Worker) |
| End-to-end happy path | Playwright (one flow: search → click → graph) |

Avoid heavy snapshot testing. The UI will churn early.

## Definition of done

- [ ] All four pages load real data with no console errors
- [ ] Force-directed graph renders 200 nodes at 60fps on a mid-range laptop
- [ ] Search debouncing prevents storming the backend
- [ ] Production build succeeds (`npm run build`)
- [ ] No telemetry, no CDN fonts, no Google APIs (privacy invariant)

## Watch-outs

- **CORS in dev only.** Don't ship a permissive CORS middleware to P6 production — the bundle is same-origin once mounted.
- **Don't render the full graph at once.** Limit to ~500 visible nodes; let the user expand neighborhoods on click.
- **Time zones.** Backend stores UTC; display in `Intl.DateTimeFormat(navigator.language)`. Pick once and document it.

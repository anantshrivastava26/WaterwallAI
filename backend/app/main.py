from fastapi import FastAPI

from .api import health, ingest, search, summary
from .config import settings

app = FastAPI(title="WaterwallAI", version="0.1.0")

app.include_router(health.router)
app.include_router(ingest.router, prefix="/ingest", tags=["ingest"])
app.include_router(search.router, prefix="/search", tags=["search"])
app.include_router(summary.router, prefix="/summary", tags=["summary"])


@app.get("/")
def root() -> dict:
    return {"app": "WaterwallAI", "env": settings.app_env}

import logging
from uuid import uuid4

from fastapi import FastAPI, Request

from .api import health, ingest, search, summary
from .config import settings

app = FastAPI(title="WaterwallAI", version="0.1.0")

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
)


@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid4())
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response

app.include_router(health.router)
app.include_router(ingest.router, prefix="/ingest", tags=["ingest"])
app.include_router(search.router, prefix="/search", tags=["search"])
app.include_router(summary.router, prefix="/summary", tags=["summary"])


@app.get("/")
def root() -> dict:
    return {"app": "WaterwallAI", "env": settings.app_env}

import logging
from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI, Request

from .api import health, ingest, search, summary
from .config import settings
from .db import models as _models
from .db.session import Base, engine


@asynccontextmanager
async def lifespan(_app: FastAPI):
    Base.metadata.create_all(engine)
    yield


app = FastAPI(title="WaterwallAI", version="0.1.0", lifespan=lifespan)

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

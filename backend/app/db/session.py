from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from ..config import settings

# Ensure local sqlite parent directory exists (e.g. ./data/waterwall.sqlite).
sqlite_path = Path(settings.sqlite_path)
if not sqlite_path.is_absolute():
    sqlite_path = Path.cwd() / sqlite_path
sqlite_path.parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(f"sqlite:///{settings.sqlite_path}", future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass

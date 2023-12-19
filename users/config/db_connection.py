from contextlib import contextmanager
from typing import Any, Dict

from sqlalchemy import create_engine
from sqlalchemy.types import JSON
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from config.settings.base import DB_USERNAME, DB_PASSWORD, DB_HOST, DATABASE

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DATABASE}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True, pool_recycle=300)
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)


class Base(DeclarativeBase):
    type_annotation_map = {
        Dict[str, Any]: JSON
    }


session = SessionLocal()


@contextmanager
def get_db():
    session.expire_on_commit = False
    try:
        yield session
    finally:
        session.expire_on_commit = False
        session.close()

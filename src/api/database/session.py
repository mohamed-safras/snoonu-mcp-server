from contextlib import contextmanager
from typing import Iterator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.config.settings import settings

engine = create_engine(
    settings.db_url,
    pool_size=settings.db_pool_size,
    max_overflow=settings.db_max_overflow,
    pool_recycle=settings.db_pool_recycle,
    pool_pre_ping=True,
)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

@contextmanager
def get_session() -> Iterator[Session]:
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
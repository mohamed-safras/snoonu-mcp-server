from contextlib import contextmanager
from typing import Iterator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.config.settings import settings

engine = create_engine(settings.db_url, pool_size=5, pool_pre_ping=True)
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
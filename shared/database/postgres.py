import os
from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


Base = declarative_base()


@lru_cache(maxsize=1)
def _session_factory():
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL must be set to connect to the database")

    engine = create_engine(database_url)
    return sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    db = _session_factory()()
    try:
        yield db
    finally:
        db.close()
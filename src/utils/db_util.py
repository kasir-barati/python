# pyright: reportUnknownMemberType=false, reportAttributeAccessIssue=false, reportUnknownMemberType=false

from functools import lru_cache

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.orm.session import Session

from .config import Settings

Base = declarative_base()
Session = sessionmaker()


# Cached the env variables to prevent reading it from FS over and over.
@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
engine = create_engine(settings.postgres_uri)


def get_session():
    Session.configure(bind=engine)

    return Session()


def init_database_connection():
    Base.metadata.bind = engine
    Session.configure(bind=engine)
    Base.metadata.create_all(engine)


def cleanup_database_connection():
    engine.dispose()

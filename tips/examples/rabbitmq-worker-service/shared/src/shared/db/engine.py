from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker


# Takes a url as an argument rather than reading an env var at import time.
# Then clients can each point it at their own database without monkeypatching module state.
def create_db_engine(database_url: str) -> Engine:
    return create_engine(database_url)


def create_session_factory(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(bind=engine, expire_on_commit=False)

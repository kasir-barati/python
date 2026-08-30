from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from shared_db.models import Base


# Takes a url as an argument rather than reading an env var at import time.
# Then clients can each point it at their own database without monkeypatching module state.
def create_db_engine(database_url: str) -> Engine:
    return create_engine(database_url)


def init_db(engine: Engine) -> None:
    # create_all is idempotent (`checkfirst=True` by default).
    # Fine for a dummy example.
    # A real project would use Alembic migrations instead: https://alembic.sqlalchemy.org/en/latest/tutorial.html
    Base.metadata.create_all(bind=engine)


def create_session_factory(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(bind=engine, expire_on_commit=False)

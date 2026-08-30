# Alembic migration configuration file
# Its job is to tell Alembic:
# 
# 1. Which database to connect to?
# 2. Which SQLAlchemy models represent your database schema?
# 3. How to compare your models with the actual database?
# 4. How to run migrations either offline or online?

import os
from logging.config import fileConfig

from alembic import context  # Think of context as the object Alembic gives your env.py to interact with the current migration operation.
from sqlalchemy import engine_from_config, pool

from shared.db import Base


config = context.config

# 👇 Alembic can configure its logging from the configuration file (alembic.ini).
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Represents the schema described by your Python models.
target_metadata = Base.metadata


def get_db_connection_string() -> str:
    configured_url = config.get_main_option("sqlalchemy.url")
    if configured_url:
        return configured_url

    return os.environ.get(
        "DATABASE_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/app"
    )


def run_migrations_offline() -> None:
    """
    This defines the function Alembic uses when running in offline mode.
    - Generates migration SQL without actually connecting to the database.
    - Generates SQL that you can inspect or execute separately.
    """
    context.configure(
        url=get_db_connection_string(),
        # 👇 One of the most important lines in the entire file. `Base.metadata` contains information about the tables defined by your SQLAlchemy models.
        target_metadata=target_metadata,
        # 👇 This tells SQLAlchemy/Alembic to put parameter values directly into generated SQL where appropriate instead of using placeholders.
        # Instead of `SELECT * FROM users WHERE id = :id` it will `SELECT * FROM users WHERE id = 123`
        # Useful when generating SQL for offline migrations
        literal_binds=True,
        # 👇 How parameters should be represented? It will use
        # SELECT * FROM users WHERE email = :email
        # Instead of "qmark": SELECT * FROM users WHERE id = ?
        # Or "format": SELECT * FROM users WHERE id = %s
        # Or "numeric": SELECT * FROM users WHERE name = :1s
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Online mode means Alembic actually connects to the database.
    """
    # 👇 If no configuration section exists, use an empty dictionary.
    configuration = config.get_section(config.config_ini_section) or {}
    # 👇 Override the configured value from alembic.ini
    configuration["sqlalchemy.url"] = get_db_connection_string()
    # 👇 Create a SQLAlchemy Engine, something Alembic can use to connect to the database.
    connectable = engine_from_config(
        # 👇 This gives SQLAlchemy the configuration dictionary.
        configuration,
        # 👇 Look for configuration options beginning with sqlalchemy.
        prefix="sqlalchemy.",
        # 👇 Normally SQLAlchemy can maintain a pool of database connections.
        # But Alembic generally doesn't need a persistent connection pool for its migration process.
        # Don't maintain a reusable connection pool.
        poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():  # 👈 Start a transaction around the migration
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

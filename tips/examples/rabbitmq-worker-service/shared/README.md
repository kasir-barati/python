# Shared Library Layout

## Package Identity

The directory, the distribution name, and the import name are all the same string on purpose:

- Directory: `shared/`
- Distribution name (`shared/pyproject.toml`): `shared`
- Import name: `shared` (package root at `shared/src/shared/`)

> [!IMPORTANT]
>
> Creating a directory called `shared` inside src is intentional. In fact that is why you can write imports like this:
>
> ```py
> from shared.db.user.repository import UserRepository
> ```

## `src/shared/db`

Everything related to persistence lives here.

```
./shared/src/shared/db/
    __init__.py     # re-exports Base and imports every entity's model
    base.py         # the single DeclarativeBase every entity's model inherits
    engine.py       # create_db_engine, create_session_factory
    user/
        __init__.py
        model.py        # the User ORM model
        repository.py   # UserRepository
```

- `Base` is not owned by any one entity: every entity's model needs to inherit the same `DeclarativeBase` so they all register on one `MetaData` object, which is what lets Alembic autogenerate compare the *whole* schema against the database in one pass.
- Each entity gets its own subpackage under `db/` holding both its model and its repository together (`db/user/model.py`, `db/user/repository.py`).
  - Alembic's `env.py` only sees tables belonging to models that have actually been imported somewhere before `Base.metadata` is read. With per-entity model files it is mandatory to have `db/__init__.py` as the single place responsible for importing every entity's model module for its registration side effect:
    ```python
    from shared.db.base import Base
    from shared.db.user.model import User  # noqa: F401  registers `users` on Base.metadata

    __all__ = ["Base", "User"]
    ```
    `shared/migrations/env.py` imports `Base` from `shared.db` (not `shared.db.base`) specifically so it goes through this file and picks up every registered entity, not just the one it happens to import directly. Adding a new entity means adding its import here too, or `alembic revision --autogenerate` will silently produce an empty diff for it.

## Adding a new Module

A future concern unrelated to persistence (e.g. shared datetime helpers) is a sibling of `db/`, not something bolted onto it:

```
shared/src/shared/
    db/
        ...
    datetime_utils.py
```

imported as `from shared.datetime_utils import ...`. It only graduates into its own subpackage (`datetime_utils/`) the day it actually needs more than one file, the same rule `db/` followed before it grew per-entity subpackages.

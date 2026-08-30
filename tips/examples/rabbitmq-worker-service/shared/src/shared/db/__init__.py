from shared.db.base import Base
from shared.db.user.model import User  # noqa: F401  registers `users` on Base.metadata for Alembic autogenerate

__all__ = ["Base", "User"]

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from shared_db.models import User


class UserRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, email: str) -> User:
        user = User(email=email)
        self._session.add(user)
        self._session.flush()
        return user

    def get_by_email(self, email: str) -> User | None:
        return self._session.scalar(select(User).where(User.email == email))

    def get_or_create(self, email: str) -> User:
        # Idempotent by construction: reprocessing the same email (e.g. a
        # RabbitMQ redelivery after a crash) returns the existing row
        # instead of inserting a duplicate.
        existing = self.get_by_email(email)
        if existing is not None:
            return existing
        return self.create(email)

    def count_by_email(self, email: str) -> int:
        return (
            self._session.scalar(
                select(func.count()).select_from(User).where(User.email == email)
            )
            or 0
        )

    def list_all(self) -> list[User]:
        return list(self._session.scalars(select(User).order_by(User.id)))

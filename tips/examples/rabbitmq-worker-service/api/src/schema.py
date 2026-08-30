import os
from collections.abc import AsyncGenerator

import redis.asyncio as aioredis
import strawberry
from shared.db.engine import create_db_engine, create_session_factory
from shared.db.user.repository import UserRepository


REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
REDIS_CHANNEL = "queue_messages"
DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/app"
)
_engine = create_db_engine(DATABASE_URL)

# ⚠️ Schema migrations run as a deploy step before this process starts.
SessionFactory = create_session_factory(_engine)


@strawberry.type
class UserType:
    id: int
    email: str


@strawberry.type
class Query:
    @strawberry.field
    def health(self) -> str:
        return "ok"

    @strawberry.field
    def users(self) -> list[UserType]:
        with SessionFactory() as session:
            repository = UserRepository(session)
            return [
                UserType(id=user.id, email=user.email)
                for user in repository.list_all()
            ]


@strawberry.type
class Subscription:
    @strawberry.subscription
    async def queue_messages(self) -> AsyncGenerator[str, None]:
        client = aioredis.Redis.from_url(REDIS_URL)
        async with client.pubsub() as pubsub:
            await pubsub.subscribe(REDIS_CHANNEL)
            while True:
                message = await pubsub.get_message(
                    ignore_subscribe_messages=True, timeout=None
                )
                if message is not None:
                    yield message["data"].decode()


schema = strawberry.Schema(query=Query, subscription=Subscription)

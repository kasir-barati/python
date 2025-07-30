from functools import lru_cache

from aio_pika import connect_robust
from aio_pika.abc import AbstractChannel, AbstractRobustConnection

from .config import Settings

USER_CREATED_QUEUE = "user.created"
USER_UPDATED_QUEUE = "user.updated"


# Cached the env variables to prevent reading it from FS over and over.
@lru_cache
def get_settings() -> Settings:
    return Settings()


async def get_connection_channel() -> (
    tuple[AbstractRobustConnection, AbstractChannel]
):
    """
    This will return the channel and connection. Optionally you can pass your queues to register them.
    """
    settings = get_settings()
    connection = await connect_robust(settings.rabbitmq_uri)
    channel = await connection.channel()

    return (connection, channel)

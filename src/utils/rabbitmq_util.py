from functools import lru_cache

from pika import BlockingConnection, ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel

from config import Settings


# Cached the env variables to prevent reading it from FS over and over.
@lru_cache
def get_settings() -> Settings:
    return Settings()


def get_connection_channel(
    queues: list[str] | None,
) -> tuple[BlockingConnection, BlockingChannel]:
    """
    This will return the channel and connection. Optionally you can pass your queues to register them.
    """
    settings = get_settings()
    connection_params = ConnectionParameters(
        settings.rabbitmq_host, settings.rabbitmq_port
    )
    connection = BlockingConnection(connection_params)
    channel = connection.channel()

    if queues is not None:
        for queue in queues:
            channel.queue_declare(queue)

    return (connection, channel)

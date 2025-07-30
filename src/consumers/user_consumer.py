import asyncio
import json
from functools import lru_cache

from aio_pika.abc import AbstractIncomingMessage

from ..models import User
from ..utils import (
    USER_CREATED_QUEUE,
    USER_UPDATED_QUEUE,
    Settings,
    get_connection_channel,
    get_session,
)


# Cached the env variables to prevent reading it from FS over and over.
@lru_cache
def get_settings() -> Settings:
    return Settings()


async def user_created_handler(
    message: AbstractIncomingMessage,
) -> None:
    print("Creating new user...")
    created_user = json.loads(message.body.decode())
    session = get_session()
    user = User(**created_user)
    session.add(user)
    session.commit()
    session.close()
    await message.ack()


async def user_updated_handler(
    message: AbstractIncomingMessage,
) -> None:
    updated_user = json.loads(message.body.decode())
    session = get_session()
    user = (
        session.query(User).filter_by(id=updated_user["id"]).first()
    )

    if user is None:
        print(
            f"Could not find the user (user ID: {updated_user['id']})!"
        )
        return

    print("Updating the user...")
    user.name = updated_user["name"]
    user.email = updated_user["email"]
    user.password = updated_user["password"]
    session.commit()
    session.close()


async def start_user_consumers():
    print("Start consuming user events!")

    settings = get_settings()
    loop = asyncio.get_running_loop()
    _, channel = await get_connection_channel()

    await channel.set_qos(prefetch_count=settings.prefetch_count)

    user_created_queue = await channel.declare_queue(
        USER_CREATED_QUEUE, auto_delete=True
    )
    user_updated_queue = await channel.declare_queue(
        USER_UPDATED_QUEUE, auto_delete=True
    )

    loop.create_task(
        user_created_queue.consume(user_created_handler, no_ack=False)
    )
    loop.create_task(
        user_updated_queue.consume(user_updated_handler, no_ack=True)
    )

    asyncio.sleep(2)

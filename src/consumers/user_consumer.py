import json
import logging
from typing import cast

from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties

from ..dtos import User
from ..utils import (
    USER_CREATED_QUEUE,
    USER_UPDATED_QUEUE,
    get_connection_channel,
)

logger = logging.getLogger("uvicorn")

users: list[User] = []


def user_created_handler(
    channel: BlockingChannel,
    method: Basic.Deliver,
    properties: BasicProperties,
    body: bytes,
) -> None:
    logger.debug("<Pushing the new user to the queue>" * 80)
    created_user = cast(User, json.loads(body.decode()))
    users.append(created_user)
    channel.basic_ack(delivery_tag=method.delivery_tag)


def user_updated_handler(
    channel: BlockingChannel,
    method: Basic.Deliver,
    properties: BasicProperties,
    body: bytes,
) -> None:
    updated_user = cast(User, json.loads(body.decode()))
    user = next(
        (u for u in users if u["id"] == updated_user["id"]), None
    )

    if user is None:
        logger.warning(
            f"Could not find the user (user ID: {updated_user['id']})!"
        )
        return

    user_index = next(
        index
        for index in range(len(users))
        if users[index]["id"] == updated_user["id"]
    )

    users[user_index] = {**users[user_index], **updated_user}


def start_user_consumers():
    _, channel = get_connection_channel(
        [USER_CREATED_QUEUE, USER_UPDATED_QUEUE]
    )

    channel.basic_consume(USER_CREATED_QUEUE, user_created_handler)
    channel.basic_consume(
        queue=USER_UPDATED_QUEUE,
        on_message_callback=user_updated_handler,
        auto_ack=True,
    )
    channel.start_consuming()

import json

from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties

from ..models import User
from ..utils import (
    USER_CREATED_QUEUE,
    USER_UPDATED_QUEUE,
    get_connection_channel,
    get_session,
)


def user_created_handler(
    channel: BlockingChannel,
    method: Basic.Deliver,
    _properties: BasicProperties,
    body: bytes,
) -> None:
    print("Creating new user...")
    created_user = json.loads(body.decode())
    session = get_session()
    user = User(**created_user)
    session.add(user)
    session.commit()
    channel.basic_ack(delivery_tag=method.delivery_tag)
    session.close()


def user_updated_handler(
    _channel: BlockingChannel,
    _method: Basic.Deliver,
    _properties: BasicProperties,
    body: bytes,
) -> None:
    updated_user = json.loads(body.decode())
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


def start_user_consumers():
    print("Start consuming user events!")

    _, channel = get_connection_channel(
        [USER_CREATED_QUEUE, USER_UPDATED_QUEUE]
    )

    channel.basic_consume(USER_CREATED_QUEUE, user_created_handler)
    channel.basic_consume(
        queue=USER_UPDATED_QUEUE,
        on_message_callback=user_updated_handler,
        auto_ack=True,
    )
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Gracefully shutting down user consumer...")
        channel.stop_consuming()

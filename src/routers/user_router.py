import json
import logging
from typing import cast
from uuid import UUID, uuid4

from fastapi import APIRouter
from pika import BasicProperties, DeliveryMode

from ..dtos import CreateUserRequest, UsersResponse
from ..models import User
from ..utils import (
    USER_CREATED_QUEUE,
    USER_UPDATED_QUEUE,
    get_connection_channel,
    get_session,
)

user_router = APIRouter()
logger = logging.getLogger("uvicorn")
_, channel = get_connection_channel(
    queues=[
        USER_CREATED_QUEUE,
        USER_UPDATED_QUEUE,
    ]
)


@user_router.get(path="/users", response_model=UsersResponse)
async def get_users(skip: int = 0, limit: int = 10) -> UsersResponse:
    session = get_session()
    users = session.query(User.id, User.email, User.name).all()
    data = [user._asdict() for user in users]
    session.close()

    return {
        "data": [
            json.loads(json.dumps(user, default=str)) for user in data
        ],
        "limit": limit,
        "skip": skip,
    }


# TODO: Refactor this so that we are following the POST-PUT Creation, http://restalk-patterns.org/post-put.html
@user_router.put("/users/", response_model=str)
@user_router.put("/users/{user_id}", response_model=str)
async def upsert_user(
    request_body: CreateUserRequest,
    user_id: UUID | None = None,
) -> str:
    logger.info(request_body)

    if user_id is None:
        logger.info("Inserting a new record in database...")
        user_id = uuid4()
        channel.basic_publish(
            exchange="",
            routing_key=USER_CREATED_QUEUE,
            body=json.dumps(
                obj={"id": user_id, **request_body.model_dump()},
                default=str,
            ),
            properties=BasicProperties(
                delivery_mode=DeliveryMode.Persistent
            ),
        )
    else:
        logger.info("Updating the existing record in database...")
        channel.basic_publish(
            exchange="",
            routing_key=USER_UPDATED_QUEUE,
            body=json.dumps(
                obj={"id": user_id, **request_body.model_dump()},
                default=str,
            ),
            properties=BasicProperties(
                delivery_mode=DeliveryMode.Persistent
            ),
        )

    return str(user_id)

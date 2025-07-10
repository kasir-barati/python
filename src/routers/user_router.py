import logging
from uuid import UUID, uuid4

from fastapi import APIRouter

from ..dtos import CreateUserRequest, UsersResponse

user_router = APIRouter()
logger = logging.getLogger("uvicorn")


@user_router.get(path="/users")
async def users(skip: int = 0, limit: int = 10) -> UsersResponse:
    return {
        "data": [{"id": str(uuid4())}],
        "limit": limit,
        "skip": skip,
    }


# TODO: Refactor this so that we are following the POST-PUT Creation, http://restalk-patterns.org/post-put.html
@user_router.put("/users/")
@user_router.put("/users/{user_id}")
async def upsert_user(
    request_body: CreateUserRequest,
    user_id: UUID | None = None,
) -> str:
    logger.info(request_body)

    if user_id is None:
        logger.info("Inserting a new record in database...")
        user_id = uuid4()
    else:
        logger.info("Updating the existing record in database...")

    return str(user_id)

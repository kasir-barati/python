import logging
from functools import lru_cache
from typing import Annotated
from uuid import UUID, uuid4

from fastapi import FastAPI, Path, Query

from config import Settings
from dtos import (
    CreateUserRequest,
    DiscountsResponse,
    FilterDiscounts,
    FilterOrders,
    IndexResponse,
    OrdersResponse,
    ProductsResponse,
    UsersResponse,
)
from utils import json_param


# Cached the env variables to prevent reading it from FS over and over.
@lru_cache
def get_settings() -> Settings:
    return Settings()


# FastAPI provides all the functionality for your API.
app = FastAPI()
settings = get_settings()
logger = logging.getLogger("uvicorn")


# The path refers to what comes after "authority". AKA endpoint/route.
@app.get(path="/")
async def index() -> IndexResponse:
    return {"message": f"Hello from {settings.app_name}"}


@app.post(path="/orders/{order_id}/refund", status_code=200)
async def refund_order(
    order_id: Annotated[
        UUID,
        Path(
            alias="orderId",
            title="Order ID",
            description="The ID of order.",
        ),
    ],
) -> None:
    logger.info(f"Refunding {order_id}...")


@app.get(path="/orders")
async def orders(
    filter: FilterOrders = json_param("filter", FilterOrders),
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(gt=0, le=10)] = 1,
) -> OrdersResponse:
    logger.info(f"Skips {skip} pages, returns only {limit} records.")
    logger.info(f"Finding order number: {filter.order_number}")
    logger.info(
        f"filter orders based when user ID is {filter.user_id}"
    )
    logger.info(
        f"filter orders based when it's been created at {filter.created_at}"
    )
    return {"data": []}


@app.get(path="/users")
async def users(skip: int = 0, limit: int = 10) -> UsersResponse:
    return {
        "data": [{"id": str(uuid4())}],
        "limit": limit,
        "skip": skip,
    }


@app.put("/users/")
@app.put("/users/{user_id}")
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


@app.get(path="/products")
async def products(
    sku: Annotated[
        str,
        Query(
            title="Stock keeping unit",
            pattern=r"^[A-Z]{3}-\d{4}$",
            description="SKU should consist of three uppercase letters followed by a hyphen and four digits.",
        ),
    ],
) -> ProductsResponse:
    logger.info(f"Filters: {filter}")
    return {"data": [{"id": str(uuid4()), "sku": sku}]}


@app.get("/discounts")
async def discounts(
    filter: Annotated[FilterDiscounts, Query()],
) -> DiscountsResponse:
    logger.info(f"Filter discounts based on: {filter}")

    return {"data": []}

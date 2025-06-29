import logging
from functools import lru_cache
from uuid import UUID, uuid4

from fastapi import FastAPI

from config import Settings
from dtos import IndexResponse, UsersResponse, OrdersResponse, FilterOrders
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
async def refund_order(order_id: UUID) -> None:
    logger.info(f"Refunding {order_id}...")


@app.get(path="/orders")
async def orders(
    filter: FilterOrders = json_param("filter", FilterOrders)
) -> OrdersResponse:
    logger.info(f"Finding order number: {filter.order_number}")
    logger.info(f"filter orders based when user ID is {filter.user_id}")
    logger.info(f"filter orders based when it's been created at {filter.created_at}")
    return {"data": []}


@app.get(path="/users")
async def users(skip: int = 0, limit: int = 10) -> UsersResponse:
    return {"data": [{"id": str(uuid4())}], "limit": limit, "skip": skip}

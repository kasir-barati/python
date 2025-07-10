import logging
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Path, Query

from ..dtos import FilterOrders, OrdersResponse
from ..utils.json_param_util import json_param

order_router = APIRouter()
logger = logging.getLogger("uvicorn")


@order_router.post(path="/orders/{order_id}/refund", status_code=200)
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


@order_router.get(path="/orders")
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

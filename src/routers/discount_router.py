import logging
from typing import Annotated

from fastapi import APIRouter, Query

from ..dtos import DiscountsResponse, FilterDiscounts

discount_router = APIRouter()
logger = logging.getLogger("uvicorn")


@discount_router.get("/discounts")
async def discounts(
    filter: Annotated[FilterDiscounts, Query()],
) -> DiscountsResponse:
    logger.info(f"Filter discounts based on: {filter}")

    return {"data": []}

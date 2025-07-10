import logging
from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Query

from ..dtos import ProductsResponse

product_router = APIRouter()
logger = logging.getLogger("uvicorn")


@product_router.get(path="/products")
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

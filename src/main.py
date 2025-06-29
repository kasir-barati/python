import logging
from functools import lru_cache
from typing import TypedDict
from uuid import UUID

from fastapi import FastAPI

from config import Settings


# Cached the env variables to prevent reading it from FS over and over.
@lru_cache
def get_settings() -> Settings:
    return Settings()


class IndexResponse(TypedDict):
    message: str


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

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI

from .consumers import start_user_consumers
from .routers import (
    discount_router,
    index_router,
    order_router,
    product_router,
    user_router,
)
from .utils import (
    cleanup_background_processes,
    cleanup_database_connection,
    init_database_connection,
    start_in_background,
)


@asynccontextmanager
async def lifespan(
    _app: FastAPI,
) -> AsyncGenerator[Any, Any]:
    print("Bootstrapping...")
    init_database_connection()
    start_in_background(start_user_consumers)
    yield
    print("Cleaning up...")
    cleanup_background_processes()
    cleanup_database_connection()


app = FastAPI(lifespan=lifespan)
logger = logging.getLogger("uvicorn")

app.include_router(index_router)
app.include_router(order_router)
app.include_router(user_router)
app.include_router(product_router)
app.include_router(discount_router)

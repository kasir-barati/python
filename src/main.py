import asyncio
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
    cleanup_database_connection,
    init_database_connection,
)

logger = logging.getLogger("uvicorn")


@asynccontextmanager
async def lifespan(
    _app: FastAPI,
) -> AsyncGenerator[Any, Any]:
    logger.info("Bootstrapping...")
    init_database_connection()
    asyncio.run(start_user_consumers())
    logger.info("2" * 80)
    yield
    logger.info("Cleaning up...")
    cleanup_database_connection()


app = FastAPI(lifespan=lifespan)

app.include_router(index_router)
app.include_router(order_router)
app.include_router(user_router)
app.include_router(product_router)
app.include_router(discount_router)

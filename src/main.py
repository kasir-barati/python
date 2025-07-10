import logging

from fastapi import FastAPI

from .routers import (
    discount_router,
    index_router,
    order_router,
    product_router,
    user_router,
)

# FastAPI provides all the functionality for your API.
app = FastAPI()
logger = logging.getLogger("uvicorn")


app.include_router(index_router)
app.include_router(order_router)
app.include_router(user_router)
app.include_router(product_router)
app.include_router(discount_router)

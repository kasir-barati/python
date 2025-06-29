from datetime import datetime
from typing import TypedDict
from uuid import UUID

from pydantic import BaseModel, Field


class FilterOrders(BaseModel):
    user_id: UUID | None = Field(None, alias="userId")
    created_at: datetime | None = Field(None, alias="createdAt")
    order_number: str | None = Field(None, alias="orderNumber")


class Order(TypedDict):
    id: str


class OrdersResponse(TypedDict):
    data: list[Order]

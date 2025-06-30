from typing import ClassVar, Literal, TypedDict

from pydantic import BaseModel, ConfigDict, Field


class Discount(TypedDict):
    id: str


class FilterDiscounts(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=50,
        title="Name",
        description="Name of product",
    )
    order_by: Literal["created_at", "updated_at"] = "created_at"

    model_config: ClassVar[ConfigDict] = ConfigDict(
        str_strip_whitespace=True
    )


class DiscountsResponse(TypedDict):
    data: list[Discount]

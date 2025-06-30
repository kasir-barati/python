from typing import TypedDict


class Product(TypedDict):
    id: str
    sku: str


class ProductsResponse(TypedDict):
    data: list[Product]

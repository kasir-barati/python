from functools import lru_cache

from fastapi import APIRouter

from ..config import Settings
from ..dtos import IndexResponse


# Cached the env variables to prevent reading it from FS over and over.
@lru_cache
def get_settings() -> Settings:
    return Settings()


index_router = APIRouter()
settings = get_settings()


# The path refers to what comes after "authority". AKA endpoint/route.
@index_router.get("/")
async def index() -> IndexResponse:
    return {"message": f"Hello from {settings.app_name}"}

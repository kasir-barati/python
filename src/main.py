from functools import lru_cache
from typing import TypedDict

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

# The path refers to what comes after "authority". AKA endpoint/route.
@app.get(path='/')
async def index() -> IndexResponse:
    return {'message': f'Hello from {settings.app_name}'}

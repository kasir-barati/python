from typing import TypedDict
from fastapi import FastAPI


# FastAPI provides all the functionality for your API.
app: FastAPI = FastAPI()

class IndexResponse(TypedDict):
    message: str

# The path refers to what comes after "authority". AKA endpoint/route.
@app.get(path='/')
async def index() -> IndexResponse:
    return {'message': 'Hello FastAPI'}

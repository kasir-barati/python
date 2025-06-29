# FastAPI

- Web framework for building APIs.

> [!NOTE]
>
> - Read the [official docs](https://fastapi.tiangolo.com/learn/), this is what they say about it:
>
>   > You could consider this a book, a course, the official and recommended way to learn FastAPI. :sunglasses:
>
> - Type annotations/hints as FastAPI is all based on them :slightly_smiling_face:. Actually this plays a pivotal role when you use [Pydantic](https://docs.pydantic.dev/latest/) to perform data validation. Also we will get to use `Annotated`, a powerful builtin type in FastAPI:
>
>   ```py
>   from typing import Annotated
>   def say_hello(name: Annotated[str, "this is just metadata"]) -> str:
>       return f"Hello {name}"
>   ```
>
> [Type hints cheat sheet](https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html).

## Start your 1st App

1. `uv venv .venv --python 3.12.3`.
2. `source .venv/bin/activate`.
3. `uv pip install "fastapi[standard]"` or `uv pip install fastapi` to install absolute minimum for FastAPI to work.
4. `code src/main.py`.
5. ```py
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
   ```
6. After you've created your API you can start your app with `fastapi dev src/main.py`

> [!TIP]
>
> - FastAPI has a builtin Swagger UI which you can open on `localhost:8000/docs`. You can find the link to it also in your terminal.
> - The `@app.get` is called "**path operation decorator**".
> - Learn about `POST-PUT` pattern [here](https://dev.to/kasir-barati/patch-vs-put-2pa3).
> - Use `async def` even if you're not gonna use `await` syntax since this will enable FastAPI to do some performance optimizations.

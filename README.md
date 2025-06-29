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
3. `uv pip install "fastapi[standard]"`
   - Or `uv pip install fastapi` to install absolute minimum for FastAPI to work.
   - Or `uv pip install "fastapi[all]"` to install everything.
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

## Environment Variables

- Variable that lives outside of the Python code, in the operating system.
- Settings and configurations are what we usually intend to get from env variables.
- We tend to not store them in our VCS.

### Any Value Read in Python from an Environment Variable will be a String

- `uv pip install pydantic-settings`.
- Is **case-insensitive**, i.e. `APP_NAME` is equal to `app_name`.
- With `get_settings` helper function you can easily override the env values in your tests.

### Reading a `.env` File

- `uv pip install python-dotenv`.
- This file is called a "dotenv".
- Note: files ending with `.env` should be gitignored.

## Path/Route Parameters

```py
@app.post(path="/orders/{order_id}/refund", status_code=200)
async def refund_order(order_id: int) -> None:
    pass
```

### `/users/me` & `/users/{user_id}`

- In this case we need to **first declare** the `/users/me` and then the other one. **Order matters!**
- Path operations are evaluated in the order they've been defined in code.

<table>
<thead><tr><th>Correct :white_check_mark:</th><th>Incorrect :x:</th></tr></thead>
<tbody><tr><td>

```py
@app.get("/users/me")
async def read_user_me():
    ...
@app.get("/users/{user_id}")
async def read_user(user_id: str):
    ...
```

</td><td>

```py
@app.get("/users/{user_id}")
async def read_user(user_id: str):
    # match also for /users/me, "thinking" that it's receiving a parameter user_id with a value of "me".
    ...
@app.get("/users/me")
async def read_user_me():
    ...
```

</td></tr></tbody>

</table>

## Query Parameters

Other function parameters that are not part of the path parameters are considered as a query string as long as they are not complex data types such as nested dictionaries!

> [!CAUTION]
>
> FastAPI does **NOT** accept JSON-encoded pydantic models in query strings! As dumb and stupid it sounds but it is the truth ([learn more](https://github.com/fastapi/fastapi/discussions/7919)).
>
> And even though we can work around it the final OpenAPI documentation would not be that beautiful. We loss all info related to what would be the shape of a complex query string! It simply shows as a string in Swagger UI.

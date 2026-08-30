FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /usr/local/bin/

WORKDIR /app

COPY pyproject.toml uv.lock* ./
COPY shared/ ./shared/

RUN uv sync --no-dev --no-install-project

COPY api/ ./api/

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "api.src.main:app", "--host", "0.0.0.0", "--port", "8000"]

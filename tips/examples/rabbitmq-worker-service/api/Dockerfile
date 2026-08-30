FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /usr/local/bin/

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends make \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock* Makefile ./
COPY shared/ ./shared/

RUN uv sync --no-dev --no-install-project

COPY api/ ./api/

EXPOSE 8000

CMD ["make", "start-api"]

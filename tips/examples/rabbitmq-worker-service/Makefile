SHELL         := /bin/bash
.SHELLFLAGS   := -eu -o pipefail -c
.DEFAULT_GOAL := help

.PHONY: help install run-api run-worker test db-migrate db-revision start-api
.ONESHELL:

## Show this help message
help:
	@echo "Makefile targets:"
	@echo ""
	@awk '/^## /{desc = substr($$0, 4)} /^[a-zA-Z_-]+:/{if (desc) {target = $$1; sub(/:.*/, "", target); printf "  make %-20s- %s\n", target, desc; desc = ""}}' $(MAKEFILE_LIST)
	@echo ""

## Install deps
install:
	@which uv > /dev/null || (echo "Error: uv is not installed. Please install uv: https://docs.astral.sh/uv/getting-started/installation/" && exit 1)
	uv sync

## Bootstraps the API (runs pending migrations first: the API owns schema migrations, the worker never does)
run-api: db-migrate
	uv run uvicorn api.src.main:app --reload

## Bootstraps the worker (does NOT run migrations; assumes the API's deploy step already applied them)
run-worker:
	uv run python -m worker.src.consumer

## Executes tests
test:
	uv run pytest -v

## Exports the GraphQL SDL to api/schema.graphql
api-schema:
	@echo "== exporting GraphQL schema to api/schema.graphql =="
	uv run strawberry export-schema api.src.schema:schema > api/schema.graphql
	@echo "== wrote api/schema.graphql ($$(wc -l < api/schema.graphql) lines) =="

## Applies pending Alembic migrations against DATABASE_URL (the one thing that owns schema changes)
db-migrate:
	uv run alembic -c shared/alembic.ini upgrade head

## Autogenerates a new Alembic revision from shared_db model changes, e.g. `make db-revision m="add users.name"`
db-revision:
	uv run alembic -c shared/alembic.ini revision --autogenerate -m "$(m)"

## Runs pending migrations then starts the API for real (no --reload); this is what api/Dockerfile's CMD invokes
start-api: db-migrate
	uv run uvicorn api.src.main:app --host 0.0.0.0 --port 8000

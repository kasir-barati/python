SHELL         := /bin/bash
.SHELLFLAGS   := -eu -o pipefail -c
.DEFAULT_GOAL := help

.PHONY: help install run-api run-worker test
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

## Bootstraps the API
run-api:
	uv run uvicorn api.src.main:app --reload

## Bootstraps the worker
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

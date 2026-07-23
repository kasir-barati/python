SHELL         := /bin/bash
.DEFAULT_GOAL := help

.ONESHELL:
.PHONY: start test init help schema

## Show this help message
help:
	@echo "Makefile targets:"
	@echo ""
	@awk '/^## /{desc = substr($$0, 4)} /^[a-zA-Z_-]+:/{if (desc) {target = $$1; sub(/:.*/, "", target); printf "  make %-20s- %s\n", target, desc; desc = ""}}' $(MAKEFILE_LIST)
	@echo ""

## Initialize project
init:
	@which uv > /dev/null || (echo "Error: uv is not installed. Please install uv: https://docs.astral.sh/uv/getting-started/installation/" && exit 1)
	uv sync

## Run the Strawberry app
start:
	uv run python demo.py

## Start the app and run pytest against it
test:
	make start &
	APP_PID=$$!
	trap "kill $$APP_PID 2>/dev/null || true" EXIT
	sleep 1
	uv run pytest -v test_demo.py

## Generate the SDL file for the app
schema:
	uv run python -c "from demo import schema; print(schema)" > schema.graphql

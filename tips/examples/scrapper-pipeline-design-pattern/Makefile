SHELL         := /bin/bash

.ONESHELL:
.PHONY: dev init

dev:
	docker compose up -d --wait
	uv run python src/main.py
	docker compose down -v

init:
	cp --update=none .env.example .env || true
	uv sync

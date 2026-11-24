SHELL         := /bin/bash

.ONESHELL:
.PHONY: dev down init sync-k8s check-k8s

dev:
	uv run python tools/render_compose.py
	docker compose -f compose.yml -f compose.generated.yml up --build

down:
	uv run python tools/render_compose.py
	docker compose -f compose.yml -f compose.generated.yml down -v

sync-k8s:
	uv run python tools/render_k8s.py

check-k8s:
	uv run python tools/render_k8s.py --check

init:
	cp --update=none .env.example .env || true
	uv sync

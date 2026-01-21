.ONESHELL:
.PHONY: help venv init start start_dev publish clean lint

PYTHON_VERSION = 3.12.12
VENV_PATH = .venv
PYTHON = $(shell [ -f $(VENV_PATH)/bin/python3 ] && echo $(VENV_PATH)/bin/python3 || echo python3)

help:
	@echo "Available commands:"
	@echo "  make venv          - Create a Python virtual environment and install dependencies"
	@echo "  make init          - Initializes the project (use after cloning the repo)"
	@echo "  make start         - Start the consumer application locally"
	@echo "  make publish       - Run publisher to send test messages (default: 20 messages)"
	@echo "  make publish N=50  - Run publisher with custom number of messages"
	@echo "  make clean         - Remove Python cache files"

venv: requirements.txt
	@which uv > /dev/null || (echo "Error: uv is not installed. Please install uv: https://docs.astral.sh/uv/getting-started/installation/" && exit 1)
	uv venv $(VENV_PATH) --python=$(PYTHON_VERSION)
	uv pip install -r requirements.txt -r requirements.dev.txt --python=$(PYTHON_VERSION)

init: venv
	@echo "Create .env file based on .env.example"
	rm .env 2>/dev/null || true
	cp .env.example .env
	@echo "✅ .env created."
	. $(VENV_PATH)/bin/activate
	pre-commit install

start:
	@echo "Starting RabbitMQ consumer..."
	python src/consumer.py

start_dev:
	@echo "Starting RabbitMQ consumer in development mode..."
	python -m watchfiles 'python src/consumer.py' src/

publish:
	@echo "Publishing test messages..."
	docker compose exec app python /app/src/publisher.py -n $(or $(N),20)

clean:
	@echo "Cleaning Python cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cleaned successfully"

lint:
	@echo "Running linters..."
	. $(VENV_PATH)/bin/activate
	pre-commit run --all-files
	@echo "✅ Linting passed"

.ONESHELL:

PYTHON_VERSION = 3.12
VENV_PATH = .venv
PYTHON = $(shell [ -f $(VENV_PATH)/bin/python3 ] && echo $(VENV_PATH)/bin/python3 || echo python3)

# Check for uv
ifeq (, $(shell which uv))
$(error "uv is not installed. Please install uv: https://docs.astral.sh/uv/getting-started/installation/")
endif

venv: requirements.dev.txt requirements.txt
	uv venv $(VENV_PATH) --python=$(PYTHON_VERSION)
	uv pip install -r requirements.dev.txt -r requirements.txt --python=$(PYTHON_VERSION)

start:
	. .venv/bin/activate
	watchmedo auto-restart \
		--directory=./src \
		--pattern="*.py" \
		--recursive \
		--ignore-patterns="*/dev_runner.py" \
		-- python src/dev_runner.py

.PHONY: start

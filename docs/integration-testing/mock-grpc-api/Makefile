.ONESHELL:

PYTHON_VERSION = 3.13
VENV_PATH = .venv
PYTHON = $(shell [ -f $(VENV_PATH)/bin/python3 ] && echo $(VENV_PATH)/bin/python3 || echo python3)

venv: requirements.dev.txt requirements.txt
	@which uv > /dev/null || (echo "Error: uv is not installed. Please install uv: https://docs.astral.sh/uv/getting-started/installation/" && exit 1)
	uv venv $(VENV_PATH) --python=$(PYTHON_VERSION)
	uv pip install -r requirements.dev.txt -r requirements.txt --python=$(PYTHON_VERSION)

init: venv
	. .venv/bin/activate || true
	make grpc_gen

grpc_gen:
	[ -d .venv ] && . .venv/bin/activate || true
	mkdir -p src/stubs
	$(PYTHON) -m grpc_tools.protoc -I src/proto/ \
		--pyi_out=src/stubs \
		--python_out=src/stubs \
		--grpc_python_out=src/stubs \
		src/proto/*.proto
	find src/stubs -type d -name '__pycache__' -prune -o -type d -exec sh -c 'echo "#  Do NOT edit me!" > "{}/__init__.py"' \;
	echo "import sys" >> src/stubs/__init__.py
	echo "from pathlib import Path" >> src/stubs/__init__.py
	echo "" >> src/stubs/__init__.py
	echo "sys.path.append(str(Path(__file__).parent))" >> src/stubs/__init__.py

test:
	[ -d .venv ] && . .venv/bin/activate || true
	pytest tests -v -s

.PHONY: venv init grpc_gen

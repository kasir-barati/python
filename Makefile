.ONESHELL:

PYTHON = $(shell [ -f ./.venv/bin/python3 ] && echo ./.venv/bin/python3 || echo python3)
PIP = ./.venv/bin/pip

venv/bin/activate: requirements.txt
	python3 -m venv venv
	chmod +x venv/bin/activate
	. venv/bin/activate
	$(PIP) install -r requirements.txt

venv: venv/bin/activate
	source venv/bin/activate 

grpc_gen:
	rm -rf src/stubs
	mkdir -p src/stubs
	$(PYTHON) -m grpc_tools.protoc -I src/protobufs \
		--pyi_out=src/stubs \
		--python_out=src/stubs \
		--grpc_python_out=src/stubs \
		src/protobufs/*.proto
	find src/stubs -type d -name '__pycache__' -prune -o -type d -exec sh -c 'echo "#  Do NOT edit me!" > "{}/__init__.py"' \;
	echo "import sys\nfrom pathlib import Path\nsys.path.append(str(Path(__file__).parent))" >> src/stubs/__init__.py

start_server:
	$(PYTHON) -m src.server

start_client:
	$(PYTHON) -m src.client

format:
	$(PYTHON) -m black src

clean:
	rm -rf .venv

freeze:
	pip freeze > requirements.txt

.PHONY: grpc_gen

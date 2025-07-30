.ONESHELL:

PYTHON = $(shell [ -f ./venv/bin/python3 ] && echo ./venv/bin/python3 || echo python3)
PIP =  $(shell [ -f ./venv/bin/pip ] && echo ./venv/bin/pip || echo pip3)


create_venv: requirements.txt
	python3 -m venv .venv
	chmod +x .venv/bin/activate
	source .venv/bin/activate
	$(PIP) install -r requirements.txt

activate_venv: create_venv
	source .venv/bin/activate

clean:
	rm -rf .venv

freeze:
	$(PIP) freeze > requirements.txt

start_dev:
	uvicorn src.main:app --host 0.0.0.0 --port $(APP_PORT) --reload --log-level debug

start:
	uvicorn src.main:app --host 0.0.0.0 --port $(APP_PORT) --log-level error

.PHONY: clean freeze create_venv

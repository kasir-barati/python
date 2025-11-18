.ONESHELL:

PYTHON_VERSION = 3.12
VENV_PATH = .venv
PYTHON = $(shell [ -f $(VENV_PATH)/bin/python3 ] && echo $(VENV_PATH)/bin/python3 || echo python3)

# Check for uv
ifeq (, $(shell which uv))
$(error "uv is not installed. Please install uv: https://docs.astral.sh/uv/getting-started/installation/")
endif

venv: requirements.dev.txt
	uv venv $(VENV_PATH) --python=$(PYTHON_VERSION)
	uv pip install -r requirements.dev.txt -r requirements.txt --python=$(PYTHON_VERSION)
	. .venv/bin/activate

init:
    mkdir -p secrets
	echo "someuser" > secrets/v1_rabbitmq_user
	echo "somepassword" > secrets/v1_rabbitmq_pass

clean:
	rm -rf $(VENV_PATH)

test:
	$(PYTHON) -m unittest discover -s src -p "*__test.py"

.PHONY: clean venv

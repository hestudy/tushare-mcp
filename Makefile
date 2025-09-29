PYTHON ?= python
VENV ?= .venv
ACTIVATE = source $(VENV)/bin/activate

.PHONY: venv install lint format test run

venv:
	$(PYTHON) -m venv $(VENV)

install:
	$(ACTIVATE) && pip install -e .[dev]

lint:
	$(ACTIVATE) && ruff check . && black --check .

format:
	$(ACTIVATE) && ruff check --fix . && black .

test:
	$(ACTIVATE) && pytest

run:
	$(ACTIVATE) && uvicorn service.app.main:app --host 0.0.0.0 --port 8000 --reload

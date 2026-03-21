.PHONY: run local test

VENV ?= .venv
PY := $(VENV)/bin/python
UVICORN := $(VENV)/bin/uvicorn

run local: ## Run API locally with auto-reload
	$(UVICORN) app.main:app --reload --host 0.0.0.0 --port 8000

test: ## Run unit tests (needs: pip install -r requirements-dev.txt)
	$(PY) -m pytest

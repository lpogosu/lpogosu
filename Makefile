.PHONY: help install render check lint test all

help:
	@echo "render  — переписать блок репозиториев в README"
	@echo "check   — упасть, если README разошёлся с аккаунтом"
	@echo "lint    — ruff и mypy"
	@echo "test    — pytest"
	@echo "all     — lint, test, check"

install:
	python -m pip install -e ".[dev]"

render:
	python scripts/render_profile.py

check:
	python scripts/render_profile.py --check

lint:
	python -m ruff check .
	python -m mypy

test:
	python -m pytest -q

all: lint test check

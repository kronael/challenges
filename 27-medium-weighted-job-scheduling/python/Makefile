.PHONY: all build fmt lint check test bench help
all: fmt build lint test

build:
	uv run python -c "import main"

fmt:
	uv run --with ruff ruff format .
	uv run --with ruff ruff check --select I --fix .

lint:
	uv run --with ruff ruff check .

check: fmt lint

test: build check
	uv run --with pytest pytest -v

bench:
	uv run python ../../scripts/bench.py --timeout "$${TIMEOUT:-10}" -- uv run python main.py

help:
	@echo "all    — fmt build lint test (default)"
	@echo "check  — fmt + lint"
	@echo "bench  — check output and time main.py on large cases"

.PHONY: test fmt lint check

fmt:
	uv run --with ruff ruff format .
	uv run --with ruff ruff check --select I --fix .

lint:
	uv run --with ruff ruff check .

check: fmt lint

test: check
	uv run --with pytest pytest -v

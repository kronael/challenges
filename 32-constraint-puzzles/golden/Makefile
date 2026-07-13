.PHONY: all build fmt lint check test help
all: test

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

help:
	@echo "all    — build + fmt + lint + pytest (default)"
	@echo "build  — syntax-check main.py"
	@echo "fmt    — ruff format + import sort"
	@echo "lint   — ruff check"
	@echo "check  — fmt + lint"
	@echo "test   — build + fmt + lint + pytest"

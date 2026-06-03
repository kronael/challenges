.PHONY: build fmt lint check test bench help

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
	@for f in ../cases/??_large_*.in; do \
	  printf "%-36s" "$$(basename $$f .in): "; \
	  t0=$$(date +%s%3N); \
	  timeout $${TIMEOUT:-10} uv run python main.py < "$$f" > /dev/null 2>&1; \
	  code=$$?; elapsed=$$(( $$(date +%s%3N) - t0 )); \
	  [ $$code -eq 124 ] \
	    && printf "TIMEOUT  (limit $${TIMEOUT:-10}s)\n" \
	    || printf "%dms\n" $$elapsed; \
	done

help:
	@echo "build  — syntax-check main.py"
	@echo "fmt    — ruff format + import sort"
	@echo "lint   — ruff check"
	@echo "test   — build + check + pytest (small cases only)"
	@echo "bench  — time main.py on large cases (TIMEOUT=10)"

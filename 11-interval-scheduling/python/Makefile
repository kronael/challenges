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
	@set -- ../cases/??_large_*.in; \
	  [ -e "$$1" ] || { printf "NO LARGE CASES\n"; exit 1; }
	@for f in ../cases/??_large_*.in; do \
	  printf "%-36s" "$$(basename $$f .in): "; \
	  actual=$$(mktemp); \
	  trap 'rm -f "$$actual"' 0; \
	  trap 'exit 129' 1; \
	  trap 'exit 130' 2; \
	  trap 'exit 143' 15; \
	  t0=$$(date +%s%3N); \
	  timeout -k 2 $${TIMEOUT:-10} uv run python main.py < "$$f" > "$$actual" 2>/dev/null; \
	  code=$$?; elapsed=$$(( $$(date +%s%3N) - t0 )); \
	  if [ $$code -ne 0 ] && [ $$code -ne 124 ]; then \
	    rm -f "$$actual"; \
	    printf "ERROR  (exit %d)\n" "$$code"; \
	    exit "$$code"; \
	  fi; \
	  if [ ! -f "$${f%.in}.out" ]; then \
	    rm -f "$$actual"; \
	    printf "MISSING EXPECTED OUTPUT\n"; \
	    exit 1; \
	  fi; \
	  if [ $$code -eq 0 ] && ! cmp -s "$${f%.in}.out" "$$actual"; then \
	    rm -f "$$actual"; \
	    printf "WRONG ANSWER\n"; \
	    exit 1; \
	  fi; \
	  rm -f "$$actual"; \
	  trap - 0 1 2 15; \
	  if [ $$code -eq 124 ]; then \
	    printf "TIMEOUT  (limit $${TIMEOUT:-10}s)\n"; \
	    exit 124; \
	  fi; \
	  printf "%dms\n" $$elapsed; \
	done

help:
	@echo "all    — fmt build lint test (default)"
	@echo "build  — syntax-check main.py"
	@echo "fmt    — ruff format + import sort"
	@echo "lint   — ruff check"
	@echo "test   — build + fmt + lint + pytest (small cases only)"
	@echo "bench  — check output and time main.py on large cases (TIMEOUT=10)"

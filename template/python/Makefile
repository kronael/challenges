TIMEOUT ?= 10
LARGE   := $(wildcard ../cases/??_large_*.in)

.PHONY: fmt lint check test bench

fmt:
	uv run --with ruff ruff format .

lint:
	uv run --with ruff ruff check .

check: fmt lint

test: check
	uv run --with pytest pytest -v

bench:
	@for f in $(LARGE); do \
	  printf "%-36s" "$$(basename $$f .in): "; \
	  t0=$$(date +%s%3N); \
	  timeout $(TIMEOUT) uv run python solution.py < "$$f" > /dev/null 2>&1; \
	  code=$$?; elapsed=$$(( $$(date +%s%3N) - t0 )); \
	  [ $$code -eq 124 ] \
	    && printf "TIMEOUT  (limit $(TIMEOUT)s)\n" \
	    || printf "%dms\n" $$elapsed; \
	done

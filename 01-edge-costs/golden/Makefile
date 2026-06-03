TIMEOUT ?= 10
LARGE   := $(wildcard ../cases/??_large_*.in)

.PHONY: test bench regen help

test:
	uv run --with pytest pytest -v

bench:
	@for f in $(LARGE); do \
	  printf "%-36s" "$$(basename $$f .in): "; \
	  t0=$$(date +%s%3N); \
	  timeout $(TIMEOUT) uv run python main.py < "$$f" > /dev/null 2>&1; \
	  code=$$?; elapsed=$$(( $$(date +%s%3N) - t0 )); \
	  [ $$code -eq 124 ] \
	    && printf "TIMEOUT  (limit $(TIMEOUT)s)\n" \
	    || printf "%dms  ← beat this\n" $$elapsed; \
	done

regen:
	@for f in ../cases/[0-9][0-9].in; do \
	  uv run python main.py < "$$f" > "$${f%.in}.out"; \
	  echo "  $$(basename $$f) → done"; \
	done

help:
	@echo "test   — verify golden passes all cases (small + large)"
	@echo "bench  — time golden on large cases (the target to beat)"
	@echo "regen  — regenerate .out files from golden solution"

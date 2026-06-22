.PHONY: all test bench regen help
all: test

test:
	uv run --with pytest pytest -v

bench:
	@for f in ../cases/??_large_*.in; do \
	  printf "%-36s" "$$(basename $$f .in): "; \
	  t0=$$(date +%s%3N); \
	  timeout -k 2 $${TIMEOUT:-10} uv run python main.py < "$$f" > /dev/null 2>&1; \
	  code=$$?; elapsed=$$(( $$(date +%s%3N) - t0 )); \
	  [ $$code -eq 124 ] \
	    && printf "TIMEOUT  (limit $${TIMEOUT:-10}s)\n" \
	    || printf "%dms  ← beat this\n" $$elapsed; \
	done

regen:
	@for f in ../cases/[0-9]*.in; do \
	  uv run python main.py < "$$f" > "$${f%.in}.out"; \
	  echo "  $$(basename $$f) → done"; \
	done

help:
	@echo "test   — verify golden passes the small cases"
	@echo "bench  — time golden on large cases (the target to beat)"
	@echo "regen  — regenerate .out files from golden"

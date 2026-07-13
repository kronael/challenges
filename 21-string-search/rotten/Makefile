.PHONY: all test bench help
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
	    && printf "TIMEOUT  (the trap — naive is too slow)\n" \
	    || printf "%dms\n" $$elapsed; \
	done

help:
	@echo "test   — rotten passes the SMALL cases (it is correct, just slow)"
	@echo "bench  — rotten TIMEOUTs on large cases — the wall the solver must clear"

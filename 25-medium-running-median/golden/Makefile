.PHONY: all test bench regen help
all: test

test:
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
	  printf "%dms  ← beat this\n" $$elapsed; \
	done

regen:
	@for f in ../cases/[0-9]*.in; do \
	  uv run python main.py < "$$f" > "$${f%.in}.out"; \
	  echo "  $$(basename $$f) → done"; \
	done

help:
	@echo "test   — verify golden passes the small cases"
	@echo "bench  — check output and time golden on large cases (the target to beat)"
	@echo "regen  — regenerate .out files from golden"

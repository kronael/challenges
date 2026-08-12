.PHONY: all test bench regen help
all: test

test:
	uv run --with pytest pytest -v

bench:
	uv run python ../../scripts/bench.py --timeout "$${TIMEOUT:-10}" -- uv run python main.py

regen:
	@for f in ../cases/[0-9][0-9].in; do \
	  uv run python main.py < "$$f" > "$${f%.in}.out"; \
	  echo "  $$(basename $$f) → done"; \
	done

help:
	@echo "test   — verify golden passes all cases"
	@echo "bench  — check output and time golden on large cases (the target to beat)"
	@echo "regen  — regenerate .out files from golden"

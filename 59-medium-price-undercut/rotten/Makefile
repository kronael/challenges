.PHONY: all test bench help
all: test

test:
	uv run --with pytest pytest -v

bench:
	uv run python ../../scripts/bench.py --timeout "$${TIMEOUT:-10}" -- uv run python main.py

help:
	@echo "test   — rotten passes the SMALL cases (it is correct, just slow)"
	@echo "bench  — check output; rotten TIMEOUTs on large cases — the wall the solver must clear"

.PHONY: build fmt lint check test bench help
TIMEOUT  ?= 5
LARGE    := $(wildcard ../cases/??_large_*.in)
BIN_NAME := $(shell grep '^name' Cargo.toml | head -1 | sed 's/.*= *"\(.*\)"/\1/')

build:
	cargo build

fmt:
	cargo fmt

lint:
	cargo clippy

check: fmt lint

test: build check
	cargo test

bench: build
	@for f in $(LARGE); do \
	  printf "%-36s" "$$(basename $$f .in): "; \
	  t0=$$(date +%s%3N); \
	  timeout $(TIMEOUT) ./target/debug/$(BIN_NAME) < "$$f" > /dev/null 2>&1; \
	  code=$$?; elapsed=$$(( $$(date +%s%3N) - t0 )); \
	  [ $$code -eq 124 ] \
	    && printf "TIMEOUT  (limit $(TIMEOUT)s)\n" \
	    || printf "%dms\n" $$elapsed; \
	done

help:
	@echo "build  — cargo build (debug)"
	@echo "fmt    — cargo fmt"
	@echo "lint   — cargo clippy"
	@echo "test   — build + check + cargo test (small cases only)"
	@echo "bench  — time debug binary on large cases (TIMEOUT=5)"

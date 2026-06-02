TIMEOUT  ?= 5
LARGE    := $(wildcard ../cases/??_large_*.in)
BIN_NAME := $(shell grep '^name' Cargo.toml | head -1 | sed 's/.*= *"\(.*\)"/\1/')

.PHONY: fmt lint check test bench

fmt:
	cargo fmt

lint:
	cargo clippy

check: fmt lint

test: check
	cargo test

bench: target/release/$(BIN_NAME)
	@for f in $(LARGE); do \
	  printf "%-36s" "$$(basename $$f .in): "; \
	  t0=$$(date +%s%3N); \
	  timeout $(TIMEOUT) ./target/release/$(BIN_NAME) < "$$f" > /dev/null 2>&1; \
	  code=$$?; elapsed=$$(( $$(date +%s%3N) - t0 )); \
	  [ $$code -eq 124 ] \
	    && printf "TIMEOUT  (limit $(TIMEOUT)s)\n" \
	    || printf "%dms\n" $$elapsed; \
	done

target/release/$(BIN_NAME):
	cargo build --release -q

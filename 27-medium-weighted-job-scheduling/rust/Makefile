.PHONY: all build fmt lint check test bench clean help
TIMEOUT  ?= 5
BIN_NAME := $(shell grep '^name' Cargo.toml | head -1 | sed 's/.*= *"\(.*\)"/\1/')

all: fmt build lint test

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
	python3 ../../scripts/bench.py --timeout "$(TIMEOUT)" -- ./target/debug/$(BIN_NAME)

clean:
	cargo clean

help:
	@echo "clean  — remove build artifacts"
	@echo "all    — fmt build lint test"
	@echo "check  — fmt + lint"
	@echo "bench  — check output and time debug binary on large cases"

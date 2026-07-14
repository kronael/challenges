.PHONY: all build fmt lint check test bench help
TIMEOUT ?= 5s

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

bench:
	cargo build --release --bin bench
	timeout -k 2 $(TIMEOUT) ./target/release/bench

help:
	@echo "all    — fmt build lint test (default)"
	@echo "build  — cargo build (debug)"
	@echo "fmt    — cargo fmt"
	@echo "lint   — cargo clippy"
	@echo "test   — build + fmt + lint + cargo test (stress)"
	@echo "bench  — release bench binary under timeout (override TIMEOUT=30s)"

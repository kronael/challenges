.PHONY: all build fmt lint check test bench help

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
	timeout -k 2 $(TIMEOUT) cargo run --release --bin bench

help:
	@echo "all    — fmt build lint test (default)"
	@echo "build  — cargo build (debug)"
	@echo "fmt    — cargo fmt"
	@echo "lint   — cargo clippy"
	@echo "test   — build + fmt + lint + cargo test (stress)"
	@echo "bench  — run timed release stress binary"

TIMEOUT ?= 5s

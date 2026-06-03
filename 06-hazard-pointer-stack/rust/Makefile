.PHONY: build fmt lint check test bench

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
	cargo bench

help:
	@echo "build  — cargo build"
	@echo "fmt    — cargo fmt"
	@echo "lint   — cargo clippy"
	@echo "test   — build + check + cargo test (stress test)"
	@echo "bench  — cargo bench"

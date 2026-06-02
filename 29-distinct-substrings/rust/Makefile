.PHONY: fmt lint check test bench

fmt:
	cargo fmt

lint:
	cargo clippy

check: fmt lint

test: check
	cargo test

bench:
	cargo bench

.PHONY: fmt lint check test bench clean

fmt:
	cargo fmt

lint:
	cargo clippy

check: fmt lint

test: check
	cargo test --release

bench:
	cargo run --release --bin bench

clean:
	cargo clean

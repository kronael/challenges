.PHONY: all build fmt lint check test bench clean help
TIMEOUT  ?= 5
BIN_NAME := $(shell grep '^name' Cargo.toml | head -1 | sed 's/.*= *"\(.*\)"/\1/')

# Every target builds in release for x86-64-v3, the target `make vec` grades,
# so `make test`, `make bench`, and `make vec` check one program.
export RUSTFLAGS := -C target-cpu=x86-64-v3

VEC_EXPECT := vectorized

all: fmt build lint test

build:
	cargo build --release

fmt:
	cargo fmt

lint:
	cargo clippy --release

check: fmt lint

test: build check
	cargo test --release

bench: build
	python3 ../../scripts/bench.py --timeout "$(TIMEOUT)" -- ./target/release/$(BIN_NAME)

clean:
	cargo clean

help:
	@echo "clean  — remove build artifacts"
	@echo "all    — fmt build lint test (default)"
	@echo "build  — cargo build --release for x86-64-v3"
	@echo "fmt    — cargo fmt"
	@echo "lint   — cargo clippy --release"
	@echo "check  — fmt + lint"
	@echo "test   — build + fmt + lint + cargo test --release (small cases only)"
	@echo "bench  — check output and time the release binary on large cases (TIMEOUT=5)"
	@echo "vec    — trace solve on the vec fixture and check its work runs in packed lanes"

include ../../shared/vec.mk

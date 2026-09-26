.PHONY: all build fmt lint check test bench vec-build clean help
TIMEOUT  ?= 5
BIN_NAME := $(shell grep '^name' Cargo.toml | head -1 | sed 's/.*= *"\(.*\)"/\1/')

# `make vec` grades its own release build for x86-64-v3; `make test` and
# `make bench` keep the debug build.
VEC_EXPECT := vectorized
VEC_BUILD  := vec-build
VEC_BIN    := target/release/$(BIN_NAME)

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

vec-build:
	RUSTFLAGS='-C target-cpu=x86-64-v3' cargo build --release

clean:
	cargo clean

help:
	@echo "clean  — remove build artifacts"
	@echo "all    — fmt build lint test (default)"
	@echo "build  — cargo build (debug)"
	@echo "fmt    — cargo fmt"
	@echo "lint   — cargo clippy"
	@echo "check  — fmt + lint"
	@echo "test   — build + fmt + lint + cargo test (small cases only)"
	@echo "bench  — check output and time debug binary on large cases (TIMEOUT=5)"
	@echo "vec    — trace solve on the vec fixture and check its work runs in packed lanes"

include ../../shared/vec.mk

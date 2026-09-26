.PHONY: all build fmt lint check test clean help
BIN_NAME := $(shell grep '^name' Cargo.toml | head -1 | sed 's/.*= *"\(.*\)"/\1/')

# `make test` and `make vec` check one build: shared/vec.mk compiles both in
# release for x86-64-v3, the target `make vec` grades, so code behind
# cfg(target_feature) cannot differ between what the tests check and what the
# grade traces.

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

clean:
	cargo clean

help:
	@echo "all    — fmt build lint test (default)"
	@echo "build  — cargo build --release for x86-64-v3"
	@echo "fmt    — cargo fmt"
	@echo "lint   — cargo clippy"
	@echo "check  — fmt + lint"
	@echo "test   — build + fmt + lint + cargo test --release against ../cases"
	@echo "vec    — trace solve on one fixture and check its work runs in packed lanes"
	@echo "clean  — remove build artifacts"

include ../../shared/vec.mk

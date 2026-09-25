.PHONY: all build fmt lint check test clean help

VEC_FUNCS  := solve
VEC_EXPECT := vectorized

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

clean:
	cargo clean

help:
	@echo "all    — fmt build lint test (default)"
	@echo "build  — cargo build (debug)"
	@echo "fmt    — cargo fmt"
	@echo "lint   — cargo clippy"
	@echo "check  — fmt + lint"
	@echo "test   — build + fmt + lint + cargo test against ../cases"
	@echo "vec    — compile solve for x86-64-v3 and check its loops are packed"
	@echo "clean  — remove build artifacts"

include ../../shared/vec.mk

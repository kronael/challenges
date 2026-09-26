.PHONY: all build fmt lint check test bench clean help
TIMEOUT  ?= 5
MOD_NAME := $(shell awk '/^module/{print $$2}' go.mod)
BIN      := /tmp/$(MOD_NAME)-bench

# simd/archsimd exists only under GOEXPERIMENT=simd, and GOAMD64=v3 is the
# x86-64-v3 target `make vec` grades. Every target builds with both, so
# `make test`, `make bench`, and `make vec` check one program.
export GOEXPERIMENT := simd
export GOAMD64 := v3

VEC_EXPECT := vectorized

all: fmt build lint test

build:
	go build -o /tmp/$(MOD_NAME)-build .

fmt:
	gofmt -w .

lint:
	go vet ./...

check: fmt lint

test: build check
	go test -v ./...

bench: build
	go build -o $(BIN) .
	python3 ../../scripts/bench.py --timeout "$(TIMEOUT)" -- $(BIN)

clean:
	rm -f $(MOD_NAME) $(MOD_NAME).exe /tmp/$(MOD_NAME)-build /tmp/$(MOD_NAME)-bench

help:
	@echo "clean  — remove built binaries"
	@echo "all    — fmt build lint test (default)"
	@echo "build  — go build for GOAMD64=v3"
	@echo "fmt    — gofmt"
	@echo "lint   — go vet"
	@echo "check  — fmt + lint"
	@echo "test   — build + fmt + lint + go test (small cases only)"
	@echo "bench  — check output and time binary on large cases (TIMEOUT=5)"
	@echo "vec    — trace solve on the vec fixture and check its work runs in packed lanes"

include ../../shared/vec.mk

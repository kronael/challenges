.PHONY: all build fmt lint check test bench vec-build clean help
TIMEOUT  ?= 5
MOD_NAME := $(shell awk '/^module/{print $$2}' go.mod)
BIN      := /tmp/$(MOD_NAME)-bench

# simd/archsimd exists only under GOEXPERIMENT=simd, so every target builds with
# it and a solve that imports it passes `make test` and `make bench` too.
export GOEXPERIMENT := simd

# `make vec` grades its own build for GOAMD64=v3, the x86-64-v3 target;
# `make test` and `make bench` keep the default target.
VEC_EXPECT := vectorized
VEC_BUILD  := vec-build
VEC_BIN    := /tmp/$(MOD_NAME)-vec

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

vec-build:
	GOAMD64=v3 go build -o $(VEC_BIN) .

clean:
	rm -f $(MOD_NAME) $(MOD_NAME).exe /tmp/$(MOD_NAME)-build /tmp/$(MOD_NAME)-bench $(VEC_BIN)

help:
	@echo "clean  — remove built binaries"
	@echo "all    — fmt build lint test (default)"
	@echo "build  — go build"
	@echo "fmt    — gofmt"
	@echo "lint   — go vet"
	@echo "check  — fmt + lint"
	@echo "test   — build + fmt + lint + go test (small cases only)"
	@echo "bench  — check output and time binary on large cases (TIMEOUT=5)"
	@echo "vec    — trace solve on the vec fixture and check its work runs in packed lanes"

include ../../shared/vec.mk

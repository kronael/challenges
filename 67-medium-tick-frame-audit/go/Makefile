.PHONY: all build fmt lint check test clean help
MOD_NAME := $(shell awk '/^module/{print $$2}' go.mod)

# simd/archsimd exists only under GOEXPERIMENT=simd, and GOAMD64=v3 is the
# x86-64-v3 target `make vec` grades. `go test` and `go build` both see the two,
# and `make vec` traces the binary `build` writes.
export GOEXPERIMENT := simd
export GOAMD64 := v3

VEC_EXPECT := vectorized

all: fmt build lint test

build:
	go build -o $(MOD_NAME) .

fmt:
	gofmt -w .

lint:
	go vet ./...

check: fmt lint

test: build check
	go test -v ./...

clean:
	rm -f $(MOD_NAME) $(MOD_NAME).exe

help:
	@echo "clean  — remove built binaries"
	@echo "all    — fmt build lint test (default)"
	@echo "build  — go build"
	@echo "fmt    — gofmt"
	@echo "lint   — go vet"
	@echo "check  — fmt + lint"
	@echo "test   — build + fmt + lint + go test against ../cases"
	@echo "vec    — trace solve on one fixture and check its work runs in packed lanes"

include ../../shared/vec.mk

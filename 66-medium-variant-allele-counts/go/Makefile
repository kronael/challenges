.PHONY: all build fmt lint check test clean help
MOD_NAME := $(shell awk '/^module/{print $$2}' go.mod)

# simd/archsimd exists only under GOEXPERIMENT=simd, and GOAMD64=v3 is the
# x86-64-v3 target scripts/vec_check.py builds, so `make test` runs the same
# code that `make vec` reads.
export GOEXPERIMENT := simd
export GOAMD64 := v3

VEC_FUNCS  := solve
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

clean:
	rm -f $(MOD_NAME) $(MOD_NAME).exe /tmp/$(MOD_NAME)-build

help:
	@echo "clean  — remove built binaries"
	@echo "all    — fmt build lint test (default)"
	@echo "build  — go build"
	@echo "fmt    — gofmt"
	@echo "lint   — go vet"
	@echo "check  — fmt + lint"
	@echo "test   — build + fmt + lint + go test against ../cases"
	@echo "vec    — compile solve for x86-64-v3 and check its loops are packed"

include ../../shared/vec.mk

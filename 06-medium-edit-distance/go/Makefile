.PHONY: all build fmt lint check test bench clean help
TIMEOUT  ?= 5
MOD_NAME := $(shell awk '/^module/{print $$2}' go.mod)

all: fmt build lint test

build:

fmt:
	gofmt -w .

lint:
	go vet ./...

check: fmt lint

test: build check
	go test -v ./...

bench: build
	python3 ../../scripts/bench.py --timeout "$(TIMEOUT)" -- ./$(MOD_NAME)

clean:
	rm -f $(MOD_NAME) $(MOD_NAME).exe

help:
	@echo "clean  — remove built binaries"
	@echo "all    — fmt build lint test (default)"
	@echo "build  — go build"
	@echo "fmt    — gofmt"
	@echo "lint   — go vet"
	@echo "check  — fmt + lint"
	@echo "test   — build + fmt + lint + go test (small cases only)"
	@echo "bench  — check output and time binary on large cases (TIMEOUT=5)"

.PHONY: all build fmt lint check test bench clean help
TIMEOUT  ?= 5
MOD_NAME := $(shell awk '/^module/{print $$2}' go.mod)
BIN      := /tmp/$(MOD_NAME)-bench

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
	@echo "all    — fmt build lint test"
	@echo "check  — fmt + lint"
	@echo "bench  — check output and time binary on large cases"

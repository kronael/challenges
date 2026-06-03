.PHONY: all build fmt lint check test bench help
TIMEOUT  ?= 5
LARGE    := $(wildcard ../cases/??_large_*.in)
MOD_NAME := $(shell awk '/^module/{print $$2}' go.mod)
BIN      := /tmp/$(MOD_NAME)-bench

all: fmt build lint test

build:
	go build .

fmt:
	gofmt -w .

lint:
	go vet ./...

check: fmt lint

test: build
	go test -v ./...

bench:
	@go build -o $(BIN) .
	@for f in $(LARGE); do \
	  printf "%-36s" "$$(basename $$f .in): "; \
	  t0=$$(date +%s%3N); \
	  timeout -k 2 $(TIMEOUT) $(BIN) < "$$f" > /dev/null 2>&1; \
	  code=$$?; \
	  elapsed=$$(( $$(date +%s%3N) - t0 )); \
	  if [ $$code -eq 124 ]; then \
	    printf "TIMEOUT  (limit $(TIMEOUT)s)\n"; \
	  else \
	    printf "%dms\n" $$elapsed; \
	  fi; \
	done

help:
	@echo "build  — go build"
	@echo "fmt    — gofmt"
	@echo "lint   — go vet"
	@echo "check  — fmt + lint"
	@echo "test   — build + go test (small cases only)"
	@echo "bench  — time binary on large cases (TIMEOUT=$(TIMEOUT))"

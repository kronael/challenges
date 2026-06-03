.PHONY: build fmt lint check test bench
TIMEOUT  ?= 5
LARGE    := $(wildcard ../cases/??_large_*.in)
MOD_NAME := $(shell awk '/^module/{print $$2}' go.mod)
BIN      := /tmp/$(MOD_NAME)-bench

build:
	go build .

fmt:
	gofmt -w .

lint:
	go vet ./...

check: fmt lint

test: build check
	go test -v ./...

bench: $(BIN)
	@for f in $(LARGE); do \
	  printf "%%-36s" "$$(basename $$f .in): "; \
	  t0=$$(date +%s%3N); \
	  timeout $(TIMEOUT) $(BIN) < "$$f" > /dev/null 2>&1; \
	  code=$$?; elapsed=$$(( $$(date +%s%3N) - t0 )); \
	  [ $$code -eq 124 ] \
	    && printf "TIMEOUT  (limit $(TIMEOUT)s)\n" \
	    || printf "%dms\n" $$elapsed; \
	done

$(BIN):
	go build -o $(BIN) .

help:
	@echo "build  — go build"
	@echo "fmt    — gofmt"
	@echo "lint   — go vet"
	@echo "test   — build + check + go test (small cases only)"
	@echo "bench  — time binary on large cases (TIMEOUT=5)"

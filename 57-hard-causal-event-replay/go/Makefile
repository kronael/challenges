.PHONY: all build fmt lint check test bench help
TIMEOUT  ?= 5
LARGE    := $(wildcard ../cases/??_large_*.in)
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
	@set -- ../cases/??_large_*.in; \
	  [ -e "$$1" ] || { printf "NO LARGE CASES\n"; exit 1; }
	@go build -o $(BIN) . && \
	for f in $(LARGE); do \
	  printf "%-36s" "$$(basename $$f .in): "; \
	  actual=$$(mktemp); \
	  trap 'rm -f "$$actual"' 0; \
	  trap 'exit 129' 1; \
	  trap 'exit 130' 2; \
	  trap 'exit 143' 15; \
	  t0=$$(date +%s%3N); \
	  timeout -k 2 $(TIMEOUT) $(BIN) < "$$f" > "$$actual" 2>/dev/null; \
	  code=$$?; elapsed=$$(( $$(date +%s%3N) - t0 )); \
	  if [ $$code -ne 0 ] && [ $$code -ne 124 ]; then \
	    rm -f "$$actual"; \
	    printf "ERROR  (exit %d)\n" "$$code"; \
	    exit "$$code"; \
	  fi; \
	  if [ ! -f "$${f%.in}.out" ]; then \
	    rm -f "$$actual"; \
	    printf "MISSING EXPECTED OUTPUT\n"; \
	    exit 1; \
	  fi; \
	  if [ $$code -eq 0 ] && ! cmp -s "$${f%.in}.out" "$$actual"; then \
	    rm -f "$$actual"; \
	    printf "WRONG ANSWER\n"; \
	    exit 1; \
	  fi; \
	  rm -f "$$actual"; \
	  trap - 0 1 2 15; \
	  if [ $$code -eq 124 ]; then \
	    printf "TIMEOUT  (limit $(TIMEOUT)s)\n"; \
	    exit 124; \
	  fi; \
	  printf "%dms\n" $$elapsed; \
	done

help:
	@echo "all    — fmt build lint test (default)"
	@echo "build  — go build"
	@echo "fmt    — gofmt"
	@echo "lint   — go vet"
	@echo "test   — build + fmt + lint + go test (small cases only)"
	@echo "bench  — check output and time binary on large cases (TIMEOUT=5)"

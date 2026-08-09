.PHONY: all build fmt lint check test bench clean help
CC       ?= cc
CFLAGS   ?= -std=c11 -O2 -g -Wall -Wextra
LDLIBS   ?=
TIMEOUT  ?= 5
LARGE    := $(wildcard ../cases/??_large_*.in)
C_IO_MAKEFILE := $(abspath $(lastword $(MAKEFILE_LIST)))
C_IO_DIR      := $(abspath $(dir $(C_IO_MAKEFILE)))
C_IO_CPPFLAGS := -D_POSIX_C_SOURCE=200809L -I. -I$(C_IO_DIR)
C_IO_HEADERS  := solution.h $(C_IO_DIR)/json.h $(C_IO_DIR)/harness.h

all: fmt build lint test

build: main

main: $(C_IO_MAKEFILE) $(C_IO_DIR)/main.c solution.c $(C_IO_HEADERS)
	$(CC) $(CPPFLAGS) $(C_IO_CPPFLAGS) $(CFLAGS) -o $@ $(C_IO_DIR)/main.c solution.c $(LDLIBS)

run_tests: $(C_IO_MAKEFILE) $(C_IO_DIR)/test.c solution.c $(C_IO_HEADERS)
	$(CC) $(CPPFLAGS) $(C_IO_CPPFLAGS) $(CFLAGS) -o $@ $(C_IO_DIR)/test.c solution.c $(LDLIBS)

fmt:
	@command -v clang-format >/dev/null 2>&1 \
	  && clang-format -i solution.c solution.h \
	  || echo "clang-format not installed — skipped"

lint:
	$(CC) $(CPPFLAGS) $(C_IO_CPPFLAGS) $(CFLAGS) -Wpedantic -Wshadow -Wstrict-prototypes -Werror \
	  -fsyntax-only $(C_IO_DIR)/main.c $(C_IO_DIR)/test.c solution.c

check: fmt lint

test: build check run_tests
	./run_tests

bench: build
	@set -- ../cases/??_large_*.in; \
	  [ -e "$$1" ] || { printf "NO LARGE CASES\n"; exit 1; }
	@for f in $(LARGE); do \
	  printf "%-36s" "$$(basename $$f .in): "; \
	  actual=$$(mktemp); \
	  trap 'rm -f "$$actual"' 0; \
	  trap 'exit 129' 1; \
	  trap 'exit 130' 2; \
	  trap 'exit 143' 15; \
	  t0=$$(date +%s%3N); \
	  timeout -k 2 $(TIMEOUT) ./main < "$$f" > "$$actual" 2>/dev/null; \
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

clean:
	rm -f main run_tests

help:
	@echo "all    — fmt build lint test (default)"
	@echo "build  — compile ./main"
	@echo "fmt    — clang-format in place (skipped when not installed)"
	@echo "lint   — compile every source with -Wpedantic -Wshadow -Werror"
	@echo "test   — build + fmt + lint + run ../cases (small cases only)"
	@echo "bench  — check output and time ./main on large cases (TIMEOUT=5)"
	@echo "clean  — remove built binaries"

.PHONY: all build fmt lint check test bench clean help
CC       ?= cc
CFLAGS   ?= -std=c11 -O2 -g -Wall -Wextra
LDLIBS   ?=
TIMEOUT  ?= 5
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
	python3 ../../scripts/bench.py --timeout "$(TIMEOUT)" -- ./main

clean:
	rm -f main run_tests

help:
	@echo "all    — fmt build lint test (default)"
	@echo "build  — compile ./main"
	@echo "fmt    — clang-format in place (skipped when not installed)"
	@echo "lint   — compile every source with -Wpedantic -Wshadow -Werror"
	@echo "check  — fmt + lint"
	@echo "test   — build + fmt + lint + run ../cases (small cases only)"
	@echo "bench  — check output and time ./main on large cases (TIMEOUT=5)"
	@echo "clean  — remove built binaries"

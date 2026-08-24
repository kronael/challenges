.PHONY: all build fmt lint check test bench clean help
CC       ?= cc
CFLAGS   ?= -std=c11 -O2 -g -Wall -Wextra -pthread -D_POSIX_C_SOURCE=200809L
TIMEOUT  ?= 60

all: fmt build lint test

build: stress benchmark

stress: stress.c solution.c solution.h
	$(CC) $(CFLAGS) -o $@ stress.c solution.c

benchmark: bench.c solution.c solution.h
	$(CC) $(CFLAGS) -o $@ bench.c solution.c

fmt:
	@command -v clang-format >/dev/null 2>&1 \
	  && clang-format -i *.c *.h \
	  || echo "clang-format not installed — skipped"

lint:
	$(CC) $(CFLAGS) -Wpedantic -Wshadow -Wstrict-prototypes -Werror -fsyntax-only \
	  stress.c bench.c solution.c

check: fmt lint

test: build check
	timeout -k 2 $(TIMEOUT) ./stress

bench: benchmark
	timeout -k 2 $(TIMEOUT) ./benchmark

clean:
	rm -f stress benchmark

help:
	@echo "all    — fmt build lint test (default)"
	@echo "build  — compile ./stress and ./benchmark"
	@echo "fmt    — clang-format in place (skipped when not installed)"
	@echo "lint   — compile every source with -Wpedantic -Wshadow -Werror"
	@echo "check  — fmt + lint"
	@echo "test   — build + fmt + lint + run the stress test (TIMEOUT=60)"
	@echo "bench  — run the throughput benchmark (TIMEOUT=60)"
	@echo "help   — show this message"
	@echo "clean  — remove built binaries"

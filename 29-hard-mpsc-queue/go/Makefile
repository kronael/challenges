.PHONY: all build fmt lint check test bench clean help
TIMEOUT  ?= 5
BENCHTIME ?= 1s
MOD_NAME := $(shell awk '/^module/{print $$2}' go.mod)

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
	timeout -k 2 $(TIMEOUT) go test -run '^$$' -bench=BenchmarkPushPop -benchtime=$(BENCHTIME) -count=1 ./...

clean:
	rm -f $(MOD_NAME) $(MOD_NAME).exe /tmp/$(MOD_NAME)-build /tmp/$(MOD_NAME)-bench

help:
	@echo "clean  — remove built binaries"
	@echo "all    — fmt build lint test (default)"
	@echo "build  — go build"
	@echo "fmt    — gofmt"
	@echo "lint   — go vet"
	@echo "test   — build + fmt + lint + go test (small cases only)"
	@echo "bench  — run throughput benchmark — TIMEOUT=5 BENCHTIME=1s"

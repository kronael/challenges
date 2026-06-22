.PHONY: all build fmt lint check test bench help
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
	timeout -k 2 $(TIMEOUT) go test -run '^$$' -bench=BenchmarkThroughput -benchtime=$(BENCHTIME) -count=1 ./...

help:
	@echo "all    — fmt build lint test (default)"
	@echo "build  — go build"
	@echo "fmt    — gofmt"
	@echo "lint   — go vet"
	@echo "test   — build + fmt + lint + go test (stress)"
	@echo "bench  — run throughput benchmark (TIMEOUT=5 BENCHTIME=1s)"

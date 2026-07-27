.PHONY: all build fmt lint check test clean help
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

clean:
	rm -f $(MOD_NAME) $(MOD_NAME).exe /tmp/$(MOD_NAME)-build /tmp/$(MOD_NAME)-bench

help:
	@echo "clean  — remove built binaries"
	@echo "all    — fmt build lint test (default)"
	@echo "build  — go build"
	@echo "fmt    — gofmt"
	@echo "lint   — go vet"
	@echo "check  — fmt + lint"
	@echo "test   — build + fmt + lint + go test"

.PHONY: fmt lint check test bench

fmt:
	gofmt -w .

lint:
	go vet ./...

check: fmt lint

test: check
	go test -v ./...

bench:
	go test -bench=. -benchmem ./...

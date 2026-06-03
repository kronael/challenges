# 31 — Go Memory Model

Ten short Go programs in `quizzes/`: predict each one's output and justify it from the Go memory model spec, then run it (with `-race`) to check.
Hard because without an explicit synchronisation event, a write in one goroutine is simply *not guaranteed* visible to another — even one started later — and the only valid reasoning is the formal happens-before relation.

## Teaches

- **Happens-before**: a value is only guaranteed visible across goroutines when a synchronisation edge orders the write before the read.
- **Which ops synchronise**: channel send/receive, `Mutex`, `WaitGroup`, `Once`, and ordered `sync/atomic` — nothing else (plain reads/writes do not).
- **False sharing measured**: quiz 10 benchmarks two counters on one cache line vs padded — same correctness, very different speed.

## Run
```
go run -race quizzes/NN_name.go   # predict first, write your answer in a comment
```
Source: [The Go Memory Model (go.dev/ref/mem)](https://go.dev/ref/mem)

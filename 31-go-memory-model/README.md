# 31 — Go Memory Model Quizzes

Not an algorithm challenge. Each file in `quizzes/` is a short Go program.
For each: **predict the output, then explain why** using the Go memory model spec.

Then run it. If you were wrong, read the spec until you can explain the gap.

Reference: [go.dev/ref/mem](https://go.dev/ref/mem) (rewritten 2022 — read this, not old blog posts)

---

## The rules that matter

1. **Within a single goroutine**, statements execute in the order written.
2. **Across goroutines**, the only synchronisation events that create
   happens-before are: channel send/receive, `sync.Mutex`, `sync.WaitGroup`,
   `sync.Once`, `sync/atomic` operations with explicit ordering.
3. **Without synchronisation**, a write by goroutine A is NOT guaranteed to be
   visible to goroutine B, even if B starts after A.
4. **`go` statement**: starting a goroutine happens-before the goroutine's
   first action — but the goroutine may not run immediately.
5. **Channel**: a send on a channel happens-before the corresponding receive
   completes. Closing a channel happens-before a receive of the zero value.
6. **`sync/atomic`**: `Store` with `Release` happens-before a `Load` with
   `Acquire` that observes the stored value.

---

## Quizzes

Run each quiz: `go run quizzes/NN_name.go`
Predict before running. Write your answer in a comment at the top.

| # | File | Tests |
|---|------|-------|
| 01 | unsynchronised_write.go | data race, undefined output |
| 02 | channel_ordering.go | channel as happens-before |
| 03 | waitgroup_fence.go | WaitGroup as memory barrier |
| 04 | atomic_vs_plain.go | atomic store/load vs plain |
| 05 | goroutine_start.go | goroutine start happens-before |
| 06 | once_init.go | sync.Once visibility |
| 07 | mutex_interleave.go | mutex ordering, non-obvious output |
| 08 | close_channel.go | close happens-before receive |
| 09 | select_ordering.go | select is non-deterministic |
| 10 | false_sharing_bench.go | false sharing, measure with bench |

Run the race detector on all: `go run -race quizzes/NN_name.go`
The race detector catches happens-before violations at runtime.

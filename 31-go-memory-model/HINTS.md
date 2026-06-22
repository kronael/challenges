# Hints — 31 Go Memory Model

> Spoilers. Open only when stuck.

- **Reason from happens-before, not from observed output.** A value is only
  *guaranteed* visible across goroutines when a synchronisation edge orders the
  write before the read. If you can't name the edge, the program has no guarantee
  — even if it printed the right thing every time you ran it.
- **Which operations synchronise**: channel send/receive, channel `close`,
  `Mutex` lock/unlock, `WaitGroup` `Done`/`Wait`, `sync.Once`, and properly
  ordered `sync/atomic` reads/writes. Nothing else does — plain reads/writes,
  `time.Sleep`, and the `go` statement itself establish no ordering between
  goroutines.
- **`go` starts a goroutine but does not synchronise it** against the rest of the
  program, so two goroutines' prints can interleave in any order (quiz 05), and a
  plain variable written by one may never become visible to another (quiz 01,
  quiz 04 version A).
- **`select` with multiple ready cases chooses uniformly at random** — it is not
  FIFO and not ordered by case position (quiz 09).
- **`close(c)` happens-before a receive of the zero value from `c`**, so a write
  sequenced before the close is visible to every receiver after the close (quiz
  08). A `Mutex` synchronises, but the *order* in which goroutines acquire it is
  still non-deterministic (quiz 07).
- **False sharing (quiz 10)**: when goroutines on different cores write to fields
  that share a cache line, each write invalidates the other core's copy (MESI
  cache-coherence traffic). Padding each counter onto its own 64-byte cache line
  removes the invalidation — same correctness, several times faster under
  contention. `perf c2c` on Linux can show the cache-to-cache transfers directly.

## Answer key

- **01 — Unsynchronised write**: the program often prints `42`, but the output is
  not guaranteed. `time.Sleep` is not a synchronisation event, so the plain write
  to `x` races with the read in `main`.
- **02 — Channel ordering**: always prints `done: 42`. The send on `c`
  happens-before the receive from `c` completes.
- **03 — WaitGroup fence**: always prints `[0 1 4 9 16]`. Each goroutine writes a
  disjoint index before `Done`, and `Wait` returns only after those writes are
  ordered before the print.
- **04 — Atomic vs plain read**: the plain-variable loop can run forever or
  otherwise behave unpredictably because it has a data race. The atomic loop is
  the one with the memory-ordering guarantee.
- **05 — Goroutine start ordering**: both `hello` then `world` and `world` then
  `hello` are possible. Starting goroutines does not order their prints relative
  to each other.
- **06 — sync.Once visibility**: every goroutine prints `99`. `sync.Once` orders
  the completed initializer before every returned `Do` call.
- **07 — Mutex interleave**: possible outputs are `0 0`, `1 0`, and `1 2`.
  `0 2` is not possible because the writes inside the writer goroutine are
  sequenced as `a = 1` before `b = 2`.
- **08 — Close channel**: every goroutine prints `100`. The write before
  `close(c)` is visible to receives that observe the closed channel.
- **09 — Select ordering**: either `c1: 1` or `c2: 2` can print. When multiple
  cases are ready, `select` does not prefer the first case.
- **10 — False sharing**: the padded layout should be faster under multi-core
  contention because the two atomic counters no longer share a cache line.

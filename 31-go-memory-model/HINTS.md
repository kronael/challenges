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

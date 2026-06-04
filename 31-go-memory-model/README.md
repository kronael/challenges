# 31 — Go Memory Model

**Task**: Ten short Go programs live in `quizzes/`. For each one, predict its output (and whether that output is deterministic) and write a one-line justification in the `Your answer:` comment slot. Then run it — quiz 10 is a benchmark, the rest run under `-race` — and check your prediction against what actually happens.

**Difficulty**: hard
**Time estimate**: ~45 min

## Problem

Each file in `quizzes/` is a self-contained `package main`. Some use channels,
mutexes, `WaitGroup`, `sync.Once`, atomics, `select`, or `close`; some use
nothing but a plain shared variable and `time.Sleep`. Your job, per quiz, is to
answer the questions in its header comment before running it:

- What does it print?
- Is the output deterministic, or can the same program print different things on
  different runs (or different hardware)?
- Why — what in the program (if anything) forces that result?

The hard part is that "it printed the right value on my machine" is not an
answer. A write performed by one goroutine is **not guaranteed** to be visible to
another goroutine — not even one started after the write — unless something in
the program orders them. Some constructs provide that ordering and some that look
like they should (a `time.Sleep`, the `go` statement itself, a passing `-race`
run on amd64) do not. Several quizzes are deliberate data races that *usually*
print the expected value yet are undefined behaviour; the race detector, not the
output, is the judge. Quiz 10 instead asks you to predict and then measure a
performance difference between two memory layouts that are both correct.

Treat a prediction as wrong if it relies on observed behaviour rather than a rule
that guarantees it.

## Run

```
go run -race quizzes/NN_name.go      # predict first, write your answer in the comment
go test -bench=. -benchmem -cpu=2,4,8 quizzes/10_false_sharing_bench.go  # quiz 10
```

Stuck? See `HINTS.md`.

Source: [The Go Memory Model (go.dev/ref/mem)](https://go.dev/ref/mem)

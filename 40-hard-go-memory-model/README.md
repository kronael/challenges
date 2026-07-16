# 40 — Hard — Go Concurrency Quizzes

**Task**: Ten short Go programs live in `quizzes/`. For each one, predict its
output (and whether that output is deterministic) and write a one-line
justification in the `Your answer:` comment slot. Then compile or run it as
directed below and compare your prediction with the behavior you observe.

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

For Quiz 04, identify which version is race-free and what visibility its reads
have after the store executes. Scheduler progress and termination are outside
the question.

Treat a prediction as wrong if it relies on observed behaviour rather than a rule
that guarantees it.

## Run

```
make test       # compile every quiz; race-run the quizzes that should terminate
make run QUIZ=02_channel_ordering.go
make race QUIZ=01_unsynchronised_write.go
make bench      # quiz 10
```

Quiz 04 is intentionally an analysis quiz; compile it, but do not run it without
your own timeout. `make race QUIZ=01_unsynchronised_write.go` intentionally
reports a race and exits nonzero. Quiz 10 is a benchmark and has no `main`
program output.

Stuck? See `HINTS.md`.

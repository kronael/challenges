# 33 — Lazy Evaluation and Corecursion in Python

In Haskell, `primes = sieve [2..]` defines an **infinite** list. `take 10 primes`
computes exactly the first ten — the definition is total, the consumption is lazy.
Nothing decides "how many" at definition time. Python generators give you the same
thing: `yield` produces values on demand, forever, and the consumer pulls only
what it needs.

The shift is **corecursion**: don't compute a finite answer, *define a structure*
and compose consumers over it. `primes` is `sieve(naturals(2))`. A running average
is a `scan` over an unbounded stream. You build with `itertools` combinators —
`islice`, `count`, `takewhile`, `tee` — never materialising more than asked.

## The rule

No `range(n)` where `n` is the answer size. Define infinite generators; let the
caller slice. If you are writing a `for` loop that counts up to `n` and appends to
a list, you are thinking imperatively.

## The prompt

**Your solution must be a pipeline of generators.** Define the infinite structure
first (`naturals`, `fibonacci`, `primes`), then express everything else as a
transform over a stream (`sieve`, `running_average`, `zipWith`, `unfold`).
`next(primes())` must return `2` immediately — no precomputation, no upper bound.

## Run

```
cd python && make test
```

Source: lazy evaluation & corecursion (Haskell); Python generators + `itertools`.

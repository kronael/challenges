# 33 — Lazy Evaluation and Corecursion

**Task**: Implement a set of infinite sequences and stream combinators as
on-demand generators. The caller decides how many elements to consume; nothing
is computed before it is asked for.

**Difficulty**: medium
**Time estimate**: ~30 min

## Problem

Fill in eight functions in `python/main.py`. Each returns (or transforms) a
*potentially infinite* sequence of values. None of them may take a length up
front, build a finite list, and return it — the sequence has no end, and the
consumer alone decides where to stop.

The functions and the values they produce:

- `naturals(start=0)` — `start, start+1, start+2, …` forever.
- `sieve(nums)` — given an ascending stream of integers `≥ 2`, yield the primes
  among them, in order.
- `primes()` — `2, 3, 5, 7, 11, …` forever.
- `fibonacci()` — `0, 1, 1, 2, 3, 5, 8, …` forever.
- `running_average(nums)` — for input `x₀, x₁, x₂, …` yield the average of every
  prefix: `x₀`, `(x₀+x₁)/2`, `(x₀+x₁+x₂)/3`, …, one output per input.
- `collatz(n)` — `n`, then repeatedly `n/2` if even else `3n+1`, continuing past
  `1` into the `1, 4, 2, 1, …` cycle.
- `zipWith(f, xs, ys)` — apply `f` element-wise to two (possibly infinite)
  sequences, yielding `f(x₀,y₀), f(x₁,y₁), …`.
- `unfold(f, seed)` — repeatedly apply `f` to the current state: `f(state)`
  returns `(value, next_state)` to emit `value` and continue, or `None` to stop.

The hard part is the discipline, not the math. The imperative reflex —
`for i in range(n)`, accumulate into a list, return the list — is exactly what
this challenge forbids. The tests pull only the prefix they need and expect the
stream to keep working afterward. A materialised answer would either be
impossible because the stream is infinite, or too slow because it chooses an
upper bound the caller never asked for.

This is a Python thinking exercise, not a JSON stdin/stdout challenge. There are
no case files, no large-case benchmark, and no hidden reference answer in the
solver scaffold. The tests in `python/` describe the contract; the implementation
belongs in `python/main.py`.

## Run

```
cd python && make
```

Stuck? See `HINTS.md`.

Source: lazy evaluation & corecursion (Haskell); Python generators + `itertools`

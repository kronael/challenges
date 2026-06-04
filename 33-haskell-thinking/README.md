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
consumer alone decides where to stop (e.g. by taking the first `k`).

The functions and the values they produce:

- `naturals(start=0)` — `start, start+1, start+2, …` forever.
- `sieve(nums)` — given an ascending stream of integers `≥ 2`, yield the primes
  among them, in order.
- `primes()` — `2, 3, 5, 7, 11, …` forever.
- `fibonacci()` — `0, 1, 1, 2, 3, 5, 8, …` forever.
- `running_average(nums)` — for input `x₀, x₁, x₂, …` yield the average of every
  prefix: `x₀`, `(x₀+x₁)/2`, `(x₀+x₁+x₂)/3`, …, one output per input, no growing
  list.
- `collatz(n)` — `n`, then repeatedly `n/2` if even else `3n+1`, continuing past
  `1` into the `1, 4, 2, 1, …` cycle.
- `zipWith(f, xs, ys)` — apply `f` element-wise to two (possibly infinite)
  sequences, yielding `f(x₀,y₀), f(x₁,y₁), …`.
- `unfold(f, seed)` — repeatedly apply `f` to the current state: `f(state)`
  returns `(value, next_state)` to emit `value` and continue, or `None` to stop.

The hard part is the discipline, not the math. The imperative reflex —
`for i in range(n)`, accumulate into a list, return the list — is exactly what
this challenge forbids. You must *define the infinite structure itself* and
compose transforms over it, so that `next(primes())` returns `2` immediately
with no precomputation and no upper bound chosen in advance. `running_average`
must carry its state forward, not re-sum a slice. The test that matters asserts
the streams are genuinely lazy: it pulls one element, checks it came back fast,
then keeps pulling — a materialised list would either be impossible (the stream
is infinite) or too slow.

## Run

```
cd python && make
```

Stuck? See `HINTS.md`.

Source: lazy evaluation & corecursion (Haskell); Python generators + `itertools`

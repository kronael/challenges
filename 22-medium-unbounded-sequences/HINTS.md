# Hints — 22 Medium — Lazy Evaluation and Corecursion

> Spoilers. Open only when stuck.

- **Lazy evaluation / corecursion**: define an unbounded stream that produces
  values on demand. A generator (`yield` in a `while True:` loop) gives you this
  directly — `next(primes())` returns `2` immediately with no precomputation and
  no upper bound chosen up front.
- **Pipeline composition**: express every result as a transform *over* a stream,
  never materialising more than the caller asks for. `primes = sieve(naturals(2))`
  — the sieve consumes the naturals lazily; the sieve of Eratosthenes here is a
  recursive generator: take the first element `p`, yield it, then sieve the rest
  with every multiple of `p` filtered out.
- **`running_average` is a scan, not a slice-and-divide**: carry `(count, total)`
  as state, and for each input yield `total / count`. One output per input, no
  growing list.
- **Laziness is observable**: `next(primes())` should return `2` immediately
  with no precomputation and no upper bound chosen up front. After that, the
  same generator should still be able to yield `3, 5, 7, ...`.
- **`itertools` helpers** fit the pipeline shape: `takewhile`, `tee`, `islice`,
  and `count` let you compose and split infinite streams without exhausting them.
- **`unfold` mirrors Haskell's `unfoldr`**: loop while `f(state)` returns a
  `(value, next_state)` pair, yielding the value and advancing the state; stop on
  `None`.

Source: lazy evaluation and corecursion in Haskell; Python generators and `itertools`

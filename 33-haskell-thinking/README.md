# 33 — Lazy Evaluation and Corecursion

Build `naturals`, `primes`, `fibonacci`, running averages, `zipWith`, and `unfold` as a pipeline of infinite generators — the caller decides how much to consume.
Hard because the discipline forbids the imperative reflex: no `range(n)` where `n` is the answer size, no count-and-append loop — you must *define the infinite structure* and compose transforms over it.

## Teaches

- **Lazy evaluation / corecursion**: define an unbounded stream (`primes = sieve(naturals(2))`) that produces values on demand; `next(primes())` returns 2 immediately with no precomputation.
- **Pipeline composition**: express every result as a transform over a stream (`sieve`, `scan`, `takewhile`, `tee`), never materialising more than asked.

## Run
```
cd python && make
```
Source: lazy evaluation & corecursion (Haskell); Python generators + `itertools`

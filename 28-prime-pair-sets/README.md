# 28 — Prime Pair Sets (Project Euler #60)

The primes 3, 7, 109, and 673 are remarkable: concatenating any two in either
order produces another prime (e.g. 3‖7 = 37 and 7‖3 = 73 are both prime).
Find the **lowest sum** of a set of **five primes** where every pair
concatenates to form a prime in both orders.

## Key ideas

- Build a graph where primes are nodes and an edge (p, q) exists iff both
  p‖q and q‖p are prime (use Miller-Rabin, not a plain sieve).
- The answer is the minimum-weight 5-clique in this graph.
- Backtracking with pruning on sorted candidates terminates fast in practice.

## Output

Single integer: the sum of the five primes.

```
cd python && make test   # uv run --with pytest pytest -v
cd go     && make test
cd rust   && make test
```

Source: [projecteuler.net/problem=60](https://projecteuler.net/problem=60)

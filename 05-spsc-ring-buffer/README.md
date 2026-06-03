# 05 — SPSC Ring Buffer

Single producer, single consumer, lock-free ring of capacity N (power of two); each side owns one index.
Hard not because of correctness but because the obvious layout puts `head` and `tail` on one cache line, so the two cores fight over it and the queue runs an order of magnitude slow.

## Teaches

- **False sharing**: `head` and `tail` are written by different cores every op; sharing a cache line means each write triggers a MESI invalidation on the other core, serialising the threads.
- **Padding to separate lines**: `#[repr(align(64))]` + padding puts each index on its own cache line, killing the invalidation traffic.
- **Full-vs-empty**: free-running monotonic counters masked only on slot access — empty is `head == tail`, full is `head - tail == N` — avoid the wrap ambiguity.

## Run
```
cd rust && make
cd go   && make
```
Source: [Drepper, *What Every Programmer Should Know About Memory* §6.4 (false sharing)](https://people.freebsd.org/~lstewart/articles/cpumemory.pdf)

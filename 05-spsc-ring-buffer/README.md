# 05 — SPSC Ring Buffer, False-Sharing Free

Single producer, single consumer, capacity N (power of two). Each side owns one
index. `push` returns false when full; `pop` returns None when empty. No locks.

The trap is full-vs-empty ambiguity. With a plain `head == tail` test you cannot
tell "empty" from "completely full" — both make the indices equal. The standard
fix is to let the indices run as free monotonic counters and mask only on slot
access: empty is `head == tail`, full is `head - tail == N`. (Do not reset them
to 0 each wrap — that reintroduces the ambiguity and a shadow-counter race.)

The performance trap is false sharing. `head` and `tail` are touched by
different cores every operation; if they share a cache line, each push
invalidates the consumer's line and vice versa, serialising the two threads.
Put them on separate 64-byte cache lines (`#[repr(align(64))]` + padding).

The test: producer sends 0..10M, consumer asserts each `pop` returns the next
expected value **in order** — catching any skip, duplicate, reorder, or torn
index. Backpressure forces the buffer to fill, exercising the full/empty boundary.

`make test` · `make bench` (push+pop throughput, dedicated consumer thread)

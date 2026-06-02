# 02 — Vyukov MPSC Queue

Intrusive linked-list queue: many producers `push`, one consumer `try_pop`.
Atomics only, no locks on the hot path.

The trap is the broken-link window. `push` does `prev = head.swap(node)` then
`prev.next = node` as two steps; between them the new node is the head but
unreachable from the old tail (predecessor's `next` still null). A consumer that
treats that null as "empty" loses already-enqueued messages — hence `try_pop` is
3-valued: `Item` / `Empty` / `Retry`.

Correct approach: `push` swaps head with `AcqRel`, then publishes `prev.next` with
`Release`. `try_pop` walks `tail`; if `tail.next` is null but `tail != head` a
producer is mid-enqueue — return `Retry`, never `Empty`. Only `tail == head` with
null next is truly empty.

The test: 8 producers (Barrier-synced) each push 1..=100k, then the full
**multiset** is checked — every value appears exactly 8 times and the drained
queue ends cleanly Empty (extra Item = duplication; lingering Retry after join =
stuck link; loss hangs to timeout). `make test` · `make bench` (drain throughput)

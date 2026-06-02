# 02 — Vyukov MPSC Queue

Intrusive linked-list queue: many producers `push`, one consumer `try_pop`.
Atomics only, no locks on the hot path.

The trap is the broken-link window. `push` does `prev = head.swap(node)` then
`prev.next = node` as two separate steps. Between them the new node is the
head but is unreachable from the old tail — its predecessor's `next` is still
null. A consumer that treats this null as "empty" loses messages that are
already enqueued. This is why `try_pop` is 3-valued: `Item`, `Empty`, `Retry`.

Correct approach: `push` swaps the head with `AcqRel` (so the consumer sees the
node) then publishes `prev.next` with `Release`. `try_pop` walks `tail`: if
`tail.next` is null but `tail != head`, a producer is mid-enqueue — return
`Retry`, do not report `Empty`. Only `tail == head` with null next is truly empty.

The test runs 8 producers (Barrier-synced start), each pushing 1..=100k. It
checks the full **multiset**: every value must appear exactly 8 times, and the
drained queue must end cleanly Empty (no extra Item = no duplication, no
lingering Retry after join = no stuck broken link). Loss hangs to timeout.

`make test` · `make bench` (single-consumer drain throughput)

# Hints — 02 Vyukov MPSC Queue

> Spoilers. Open only when stuck.

- **The two-step link (the broken-link window)**: `push` does
  `prev = head.swap(node)` (one atomic exchange), then `prev.next = node` (one
  store). Those two steps are *not* atomic together. In between, `node` is the
  new head but is unreachable from the tail, because `prev.next` is still null.
  That single non-atomic gap is the entire source of difficulty.

- **3-valued pop**: from the consumer's tail, read `tail.next`.
  - `tail.next != null` → that successor carries the value; advance the tail and
    return the item.
  - `tail.next == null` and `tail == head` → genuinely empty, return `Empty`.
  - `tail.next == null` and `tail != head` → a producer did the `head.swap` but
    has not yet published `prev.next`; you are inside the broken-link window.
    Return `Retry`, never `Empty`. Returning `Empty` here is the classic lost
    message.

- **Memory ordering**: the `head.swap` in `push` is `AcqRel` (it both publishes
  the new node and acquires the previous head). The `prev.next = node` publish is
  `Release`. The consumer reads `tail.next` (and `head`) with `Acquire`, so it
  sees the node's fully-initialised value once the link is observed. Plain
  `Relaxed` on these is wrong on weak-memory hardware.

- **Sentinel/stub node**: start the list with a dummy node so producers always
  have a non-null `prev` to swap against, and the consumer always has a `tail`
  to advance — no null special-casing on either side.

The wrong version that "works" single-threaded but loses messages under load
(returns `Empty` in the broken-link window) is in `rotten/main.c`.

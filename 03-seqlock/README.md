# 03 — Seqlock for a 64-byte Payload

One writer, many readers, protecting a 64-byte payload with a sequence counter.
Atomics only — readers never block the writer.

The trap is the torn read. The payload is wider than any atomic, so the writer
copies it byte by byte. A reader that copies concurrently can see some bytes
from epoch K and some from K+1 — a value that never existed. The fix is the
seqlock protocol: writer does `seq++` (now odd) → copy → `seq++` (now even);
reader loads `seq` (must be even), copies, loads `seq` again, and retries if
either load was odd or the two differ.

The ordering trap: the second reader load must `Acquire` and the writer's
trailing `seq++` must `Release`, with a `fence(Acquire)` after the copy — so the
data reads cannot be reordered past the sequence check. `Relaxed` on the checks
lets the CPU hoist the payload load outside the guarded window and tear silently.

The test: 1 writer stamps an incrementing counter into all eight u64 slots while
15 readers loop millions of times. Every accepted read must have all eight slots
**equal** — any mismatch is a torn read and the count of torn reads must be ZERO.

`make test` · `make bench` (reads/sec under write contention)

# Hints — 57 Hard — Causal Event Replay

> Spoilers. Open only when stuck.

- Map each `(process, local_sequence)` pair to its event.
- An event depends on the preceding event from its own process. For every other
  process `q`, a positive `clock[q]` adds a dependency on event
  `(q, clock[q])`.
- These dependencies form a DAG. Track each event's unmet dependency count and
  push newly eligible events into a min-heap keyed by ID.
- A vector clock records only the latest event seen from another process. Its
  earlier local events are already covered by that process's own chain.
- Repeatedly rescanning every pending event for deliverability is correct but
  quadratic. That direct pending-list loop is the rotten reference.

Sources:

- [Fidge — Timestamps in message-passing systems that preserve partial ordering](https://fileadmin.cs.lth.se/cs/Personal/Amr_Ergawy/dist-algos-papers/4.pdf)
- [Mattern — Virtual time and global states of distributed systems](https://vs.inf.ethz.ch/publ/papers/VirtTimeGlobStates.pdf)

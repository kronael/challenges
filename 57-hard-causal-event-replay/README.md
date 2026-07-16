# 57 — Hard — Causal Event Replay

**Task**: Replay shuffled distributed events without violating causality.

**Difficulty**: hard
**Time estimate**: ~90 min

## Problem

Events from several processes arrive in arbitrary order. Each event has a unique
integer `id`, its source `process`, and a vector `clock` with one entry per
process.

For an event from process `p`, `clock[p]` is its local sequence number. Every
positive `clock[q]` says that event number `clock[q]` from process `q` happened
no later than this event. Each process contains local sequence numbers `1`
through its final number without gaps.

Output an order that respects every local and cross-process dependency. When
several events are eligible, emit the event with the smallest `id`. Inputs are
guaranteed to describe a valid history.

Constraints: 1 to 32 processes and at most 200000 events.

## Input

```json
{"processes":2,"events":[{"id":30,"process":1,"clock":[1,1]},{"id":10,"process":0,"clock":[1,0]},{"id":20,"process":0,"clock":[2,0]}]}
```

## Output

Print event IDs in replay order, separated by spaces.

## Example

```text
10 20 30
```

## Run

```bash
make -C python
make -C go
make -C rust
```

Stuck? See `HINTS.md`.

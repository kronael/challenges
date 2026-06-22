# 42 — News Feed Merge

**Task**: Merge several already-time-sorted event feeds into one global timeline.

**Difficulty**: medium
**Time estimate**: ~30 min

## Problem

You are given `K` news feeds. Each feed is a list of events, and within a feed the
events are already sorted by ascending timestamp `ts`. Produce one combined stream
of all events in global timestamp order.

When two events share a timestamp, order them by which feed they came from (lower
feed index first); if they are still tied, by ascending `id`.

There can be many feeds and many events in total — concatenating everything and
sorting from scratch throws away the fact that each feed already arrives in order,
and is needlessly slow at scale. The challenge is to merge while preserving the
existing per-feed order.

Constraints: total events up to 2·10⁵ across up to ~10⁴ feeds; `ts` and `id` fit
in i64; a feed may be empty.

## Input

```json
{"feeds": [[{"ts": 1, "id": 10}, {"ts": 5, "id": 11}], [{"ts": 1, "id": 20}, {"ts": 3, "id": 21}]]}
```

Each feed is a list of `{"ts", "id"}` events sorted by `ts`.

## Output

The merged events on one line, space-separated, each emitted as `ts` then `id`:

```
1 10 1 20 3 21 5 11
```

## Examples

**Example 1** — two feeds; the `ts=1` tie breaks toward the lower feed index (10 before 20)
```
{"feeds":[[{"ts":1,"id":10},{"ts":5,"id":11}],[{"ts":1,"id":20},{"ts":3,"id":21}]]} → 1 10 1 20 3 21 5 11
```

**Example 2** — a single feed passes through unchanged
```
{"feeds":[[{"ts":1,"id":10},{"ts":5,"id":11},{"ts":9,"id":12}]]} → 1 10 5 11 9 12
```

## Run

```
cd rust   && make
cd go     && make
cd python && make
```

Stuck? See `HINTS.md`.

Source: CLRS §6.5

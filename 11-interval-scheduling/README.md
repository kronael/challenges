# 11 — Interval Scheduling

**Task**: Given N meeting requests and one room, accept as many non-overlapping meetings as possible.

**Difficulty**: medium
**Time estimate**: ~30 min

## Problem

You manage a single meeting room and have `n` requests, each with a start and end time. Book the largest set of meetings that don't overlap (touching at an endpoint is fine — the next meeting can start exactly when the last ends).

The intuitive sorts both fail: shortest-first can split a pair that would've fit, and earliest-*start*-first lets one long meeting hog the morning. The provably optimal key is earliest *end* time — finish each meeting as soon as possible to leave the most room for the rest. Why is that the right greedy?

Constraints: n up to ~10⁵, times fit in i32.

## Input

```json
{"n": 4, "intervals": [[1,3],[2,4],[3,5],[4,6]]}
```

## Output

A single integer: the maximum number of non-overlapping meetings.

## Examples

**Example 1** — taking [1,3] then [3,5] beats grabbing the overlapping [2,4]
```
{"n":4,"intervals":[[1,3],[2,4],[3,5],[4,6]]} → 2
```

**Example 2** — one long meeting vs. several short ones: earliest-end wins
```
{"n":3,"intervals":[[1,10],[2,3],[4,5]]} → 2
```

## Teaches

- **Earliest-finish-time greedy**: sort by end, take each meeting whose start ≥ the last accepted end.
- **Exchange argument**: any optimal schedule can be rewritten to start with the earliest-finishing pick without losing meetings — that's the proof of optimality.

## Run

```
cd rust   && make
cd go     && make
cd python && make
```

Source: CLRS §16.1

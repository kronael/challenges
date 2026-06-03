# 11 — Interval Scheduling

Given `n` intervals `[start, end]`, select the maximum number that are pairwise non-overlapping (touching at an endpoint does not count as overlap). The interesting part is why sorting by *end* time — not start or length — is provably optimal.

**Difficulty: medium** — one greedy with a non-obvious sort key and exchange-argument proof, solvable in ~30 min.

## Input / Output

```
{"n":<int>,"intervals":[[start,end],…]}
---
<count>      maximum number of non-overlapping intervals
```

## Example

```
{"n":4,"intervals":[[1,3],[2,4],[3,5],[4,6]]}
→ 2      e.g. [1,3] then [3,5]
```

## Teaches

- **Earliest-finish-time greedy**: sort by end, take each interval whose start is ≥ the last chosen end; finishing soonest leaves the most room for the rest.
- **Exchange argument**: any optimal solution can be transformed to start with the earliest-finishing pick without losing intervals, proving the greedy optimal.

## Run

```
cd rust   && make
cd go     && make
cd python && make
```

Source: CLRS §16.1

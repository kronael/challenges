# 08 — Longest Increasing Subsequence

Given a sequence of integers, find the length of the longest strictly increasing subsequence (elements need not be contiguous).

## Input / Output

```
{"n":<int>,"seq":[<int>,…]}
---
<length>      length of the longest strictly increasing subsequence
```

## Examples

```
{"n":8,"seq":[3,1,4,1,5,9,2,6]}
→ 4

{"n":5,"seq":[5,4,3,2,1]}
→ 1
```

## Key insight

Patience sorting: keep `tails[i]` = smallest possible tail of an increasing subsequence of length `i+1`; binary-search the insertion point for each element, giving O(n log n).

## Run

```
cd python && make test
cd go     && make test
cd rust   && make test
```

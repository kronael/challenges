# 15 — Binary Search on Answer (Book Allocation)

Split the array `pages` into `k` contiguous, non-empty groups assigned to `k` students (order preserved). Minimize the maximum total pages any single student reads. Assumes `1 ≤ k ≤ len(pages)`.

## Input / Output

```
{"k":<int>,"pages":[<int>,…]}
---
<value>      minimum possible maximum pages
```

## Examples

```
{"k":3,"pages":[12,34,67,90]}
→ 90

{"k":2,"pages":[10,20,30,40]}
→ 60
```

## Key insight

The answer is monotone: if a page cap is feasible, any larger cap is too. Binary search the cap in `[max(pages), sum(pages)]`, checking feasibility with a greedy left-to-right partition. O(n log(sum)).

## Run

```
cd python && make test
cd go     && make test
cd rust   && make test
```

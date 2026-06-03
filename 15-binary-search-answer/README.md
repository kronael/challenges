# 15 — Binary Search on Answer (Book Allocation)

Split `pages` into `k` contiguous groups, minimizing the largest group sum. The trick is that you don't search the array — you search the *answer*.

## Input / Output

```
{"k":<int>,"pages":[<int>,…]}
---
<value>      minimum possible maximum pages
```

## Example

```
{"k":2,"pages":[10,20,30,40]}
→ 60      ([10,20,30] | [40] gives max 60)
```

## Teaches

- **Optimization → decision**: rewrite "find the minimum feasible X" as "is X feasible?", a monotone predicate you can binary-search over the value range `[max, sum]`.
- **Greedy feasibility check**: a single left-to-right pass counts the groups a given cap needs — O(n) per probe, O(n log sum) overall.

## Run
```
cd rust && make
cd go   && make
cd python && make
```
Source: https://codeforces.com/edu/courses

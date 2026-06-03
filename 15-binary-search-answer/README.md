# 15 — Binary Search on the Answer

**Task**: Split textbooks into K contiguous blocks so the busiest student reads as few pages as possible.

**Difficulty**: medium
**Time estimate**: ~30 min

## Problem

Allocate N textbooks (each with a page count) across K students so the maximum pages any single student reads is minimised. Each student gets a contiguous block. You can't search the array directly — there are exponentially many splits. The insight: binary-search on the *answer* (the maximum), and for each candidate cap check feasibility in O(n).

## Input

```json
{"k": 2, "pages": [10, 20, 30, 40]}
```

## Output

A single integer: the minimum possible value of the largest block sum.

## Examples

**Example 1** — balance the small books against the big one
```
k=2, pages [10,20,30,40] → 60   ([10,20,30] | [40])
```

**Example 2** — one huge book sets a floor no split can beat
```
k=2, pages [5,5,100] → 100   ([5,5] | [100])
```

## Teaches

- **Optimization → decision**: rewrite "find the minimum feasible X" as "is X feasible?", a monotone predicate you can binary-search over `[max, sum]`.
- **Greedy feasibility check**: one left-to-right pass counts the groups a cap needs — O(n) per probe, O(n log sum) overall.

## Run

```
cd rust && make
cd go   && make
cd python && make
```

Source: https://codeforces.com/edu/courses

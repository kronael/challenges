# 15 — Binary Search on the Answer

**Task**: Split textbooks into K contiguous blocks so the busiest student reads as few pages as possible.

**Difficulty**: medium
**Time estimate**: ~30 min

## Problem

You have `N` textbooks laid out in a row, the `i`-th holding `pages[i]` pages, and
`K` students. Hand the books out so that each student gets a *contiguous* block of
the row, every book is assigned, and the row's order is preserved. Among all such
splits, minimise the largest total any single student ends up reading. Output that
minimum-possible maximum.

The catch is scale. The number of ways to cut a row of `N` books into blocks grows
exponentially, so you cannot enumerate the splits and pick the best — at `N = 2·10⁵`
that search never finishes. You need a way to home in on the answer without ever
materialising a split.

Constraints: `N` up to 2·10⁵, `K` up to `N`, page counts fit in i32, the total fits
in i64.

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

## Run

```
cd rust && make
cd go   && make
cd python && make
```

Stuck? See `HINTS.md`.

Source: https://codeforces.com/edu/courses

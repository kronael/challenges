# 12 — Medium — Textbook Split

**Task**: Split textbooks into K contiguous blocks so the busiest student reads as few pages as possible.

**Difficulty**: medium
**Time estimate**: ~30 min

## Problem

You have `N` textbooks laid out in a row, the `i`-th holding `pages[i]` pages, and
`K` students. Hand the books out so that each student gets a *contiguous* block of
the row, every book is assigned, and the row's order is preserved. Among all such
splits, minimise the largest total any single student ends up reading. Output that
minimum-possible maximum.

Constraints: `1 <= N <= 2·10^5`, `1 <= K <= N`, each page count is a positive
32-bit signed integer, and the total page count fits in a signed 64-bit integer.

## Input

```json
{"k": 2, "pages": [10, 20, 30, 40]}
```

## Output

A single integer: the minimum possible value of the largest block sum.

## Examples

**Example 1** — four books and two students
```
k=2, pages [10,20,30,40] -> 60
One optimal split is [10,20,30] | [40].
```

**Example 2** — one book is much larger than the others
```
k=2, pages [5,5,100] -> 100
One optimal split is [5,5] | [100].
```

## Run

```
make -C rust
make -C go
make -C python
```

Stuck? See `HINTS.md`.

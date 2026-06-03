# 08 — Longest Increasing Subsequence

Find the length of the longest strictly increasing subsequence of an integer sequence (elements need not be contiguous). The interesting part is beating the obvious O(n²) DP with an O(n log n) patience-sorting trick.

**Difficulty: medium** — one non-obvious algorithm (patience sort + binary search), solvable in ~30 min.

## Input / Output

```
{"n":<int>,"seq":[<int>,…]}
---
<length>      length of the longest strictly increasing subsequence
```

## Example

```
{"n":8,"seq":[3,1,4,1,5,9,2,6]}
→ 4      e.g. 1,4,5,6 or 1,4,5,9
```

## Teaches

- **Patience sorting**: maintain `tails[i]` = smallest possible tail of any increasing subsequence of length `i+1`; the array length is the answer.
- **Binary search for the insertion point**: `bisect_left` finds where each element extends or improves a pile, turning an O(n²) scan into O(n log n).

## Run

```
cd rust   && make
cd go     && make
cd python && make
```

Source: CLRS §15.4

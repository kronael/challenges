# 18 — Medium — Task Ordering

**Task**: Order tasks so every prerequisite comes before the task that needs it, or report a cycle.

**Difficulty**: medium
**Time estimate**: ~30 min

## Problem

You have `n` tasks numbered `0..n-1` with prerequisites: a directed edge `A→B`
means task `A` must complete before task `B`. Produce an ordering of all `n`
tasks in which every task appears after all of its prerequisites — like a build
system or a course schedule.

Many valid orderings can exist. Return the lexicographically smallest valid
ordering, comparing task numbers from left to right. This makes the answer
unique.

If the prerequisites contain a cycle, no valid ordering exists — output `CYCLE`.

Constraints: `n` up to `10⁵`, up to `2·10⁵` edges.

## Input

```json
{"n": 6, "edges": [[5,2],[5,0],[4,0],[4,1],[2,3],[3,1]]}
```

## Output

The lexicographically smallest valid ordering on one line, space-separated, or
`CYCLE`.

## Examples

**Example 1** — a graph with several valid orderings
```
n=6, edges [[5,2],[5,0],[4,0],[4,1],[2,3],[3,1]] → 4 5 0 2 3 1
```

**Example 2** — a mutual prerequisite has no valid order
```
n=2, edges [[0,1],[1,0]] → CYCLE
```

## Run

```
make -C rust
make -C go
make -C python
```

Stuck? See `HINTS.md`.

# 24 — Topological Sort

**Task**: Order tasks so every prerequisite comes before the task that needs it, or report a cycle.

**Difficulty**: medium
**Time estimate**: ~30 min

## Problem

You have `n` tasks numbered `0..n-1` with prerequisites: a directed edge `A→B`
means task `A` must complete before task `B`. Produce an ordering of all `n`
tasks in which every task appears after all of its prerequisites — like a build
system or a course schedule.

Many valid orderings can exist, so the output is pinned down: among the tasks
that are ready to go at each step, always pick the smallest-numbered one. This
makes the answer unique.

If the prerequisites contain a cycle, no valid ordering exists — output `CYCLE`.

Constraints: `n` up to `10⁵`, up to `2·10⁵` edges. The graph can be huge, so the
ordering must be produced in (near) linear time; re-scanning the whole graph for
the next ready task at every step is too slow at this scale.

## Input

```json
{"n": 6, "edges": [[5,2],[5,0],[4,0],[4,1],[2,3],[3,1]]}
```

## Output

A valid ordering on one line, space-separated, or `CYCLE`.

## Examples

**Example 1** — always emitting the smallest ready task makes the order deterministic
```
n=6, edges [[5,2],[5,0],[4,0],[4,1],[2,3],[3,1]] → 4 5 0 2 3 1
```

**Example 2** — a mutual prerequisite has no valid order
```
n=2, edges [[0,1],[1,0]] → CYCLE
```

## Run

```
cd rust && make
cd go   && make
cd python && make
```

Stuck? See `HINTS.md`.

Source: CLRS §22.4

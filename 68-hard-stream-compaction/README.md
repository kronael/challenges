# 68 — Hard — Sparse Activation Gate

**Task**: Given one batch of gate scores and a threshold, report the scores
that exceed the threshold, in batch order.

**Difficulty**: hard
**Time estimate**: ~60 min

## Problem

A gating layer has scored one batch of activations. `scores` holds one integer
per activation, in batch order — the gate's fixed-point output for that
activation. `threshold` is the gate's cut-off.

An activation is **kept** when its score is strictly greater than `threshold`.
A score equal to the threshold is not kept.

Report the kept scores in the order they appear in `scores`, one after
another, and nothing else.

## Two gates

`make test` checks the answer against `cases/`.

`make vec` checks the shape of the code that produced it. It compiles `solve`
for `x86-64-v3` at `-O3` and reads back the loops the compiler emitted: one of
them must carry the selection in packed SIMD lanes. A `solve` whose loops the
compiler leaves in scalar registers fails `make vec` even when every case
passes.

Both gates must pass. There are no large cases and no timing gate — this
challenge is graded on the code the compiler emits, not on elapsed time.
`make bench` has no recipes to generate here and says so.

## Constraints

- `0 ≤ len(scores) ≤ 200000`
- `-10^9 ≤ scores[i] ≤ 10^9`
- `-10^9 ≤ threshold ≤ 10^9`

## Input

```json
{"scores":[3,-1,8,5,0,9],"threshold":4}
```

## Output

One line: the kept scores in batch order, separated by single spaces. When no
score is kept, the line is empty.

```
8 5 9
```

## Examples

**Example 1** — three of six scores clear the cut-off, and they keep their batch order
```
{"scores":[3,-1,8,5,0,9],"threshold":4} → 8 5 9
```

**Example 2** — a score equal to the threshold is not kept
```
{"scores":[4,4,5],"threshold":4} → 5
```

**Example 3** — nothing kept: the output is an empty line
```
{"scores":[1,2,3],"threshold":3} →
```

## Run

From the challenge directory:

```
make -C c test
make -C c vec
make -C rust test
make -C rust vec
```

The C solver directory builds for `x86-64-v3`, the same target `make vec`
grades, so running `make test` needs a machine with AVX2.

> No debug prints. Extra stdout breaks the test harness and signals you don't
> have a mental model yet. Build the model, then write the code.

Stuck? See `HINTS.md`.

# 66 — Medium — Variant Allele Counts

**Task**: Given one variant's per-sample calls, report the alternate-allele
count and the called-allele count over the samples that clear a depth and a
quality threshold.

**Difficulty**: medium
**Time estimate**: ~30 min

## Problem

A variant caller has genotyped one position across a cohort. `samples` holds one
entry per sample, in cohort order. An entry is either a call —

- `genotype` — how many alternate alleles the sample carries: `0`, `1`, or `2`
- `depth` — how many reads the call rests on
- `quality` — how confident the caller is in it

— or `null`, meaning the caller produced no call for that sample.

A sample **passes** when it has a call, its `depth` is at least `min_depth`, and
its `quality` is at least `min_quality`. Both thresholds are inclusive. A sample
with no call never passes, whatever the thresholds are.

Report two numbers over the passing samples:

- `AC` — the sum of their `genotype` values
- `AN` — two per passing sample

## Two gates

`make test` checks the answer against `cases/`.

`make vec` checks the shape of the code that produced it. It compiles `solve`
for `x86-64-v3` at `-O3` and reads back the loops the compiler emitted: one of
them must carry the whole arithmetic of the aggregation in packed SIMD lanes. A
`solve` whose loops the compiler leaves in scalar registers fails `make vec`
even when every case passes.

Both gates must pass. There are no large cases and no timing gate — this
challenge is graded on the code the compiler emits, not on elapsed time.
`make bench` has no recipes to generate here and says so.

## Constraints

- `0 ≤ len(samples) ≤ 200000`
- `genotype ∈ {0, 1, 2}`
- `0 ≤ depth ≤ 10^6` and `0 ≤ quality ≤ 10^6`
- `0 ≤ min_depth ≤ 10^6` and `0 ≤ min_quality ≤ 10^6`
- `AC` and `AN` both fit in a signed 32-bit integer

## Input

```json
{"samples":[{"genotype":1,"depth":30,"quality":99},null,{"genotype":0,"depth":44,"quality":15}],"min_depth":10,"min_quality":20}
```

## Output

One line: `AC`, a single space, `AN`.

```
1 2
```

## Examples

**Example 1** — the second sample has no call, the third is under the quality floor
```
{"samples":[{"genotype":1,"depth":30,"quality":99},null,{"genotype":0,"depth":44,"quality":15}],"min_depth":10,"min_quality":20} → 1 2
```

**Example 2** — a sample sitting exactly on both thresholds passes; one read short does not
```
{"samples":[{"genotype":2,"depth":10,"quality":20},{"genotype":2,"depth":9,"quality":20}],"min_depth":10,"min_quality":20} → 2 2
```

## Run

From the challenge directory:

```
make -C c test
make -C c vec
make -C rust test
make -C rust vec
```

Both solver directories build for `x86-64-v3`, the same target `make vec`
grades, so running `make test` needs a machine with AVX2.

> No debug prints. Extra stdout breaks the test harness and signals you don't
> have a mental model yet. Build the model, then write the code.

Stuck? See `HINTS.md`.

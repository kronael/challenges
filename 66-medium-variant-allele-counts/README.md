# 66 — Medium — Variant Allele Counts

**Task**: Given one variant's per-sample dosages, depths, and qualities,
report the summed dosage and the called-allele count over the samples that
clear a depth and a quality threshold.

**Difficulty**: medium
**Time estimate**: ~30 min

## Problem

A variant caller has scored one position across a cohort. The three arrays
hold one entry per sample, in cohort order:

- `dosage` — the expected number of alternate alleles the sample carries, a
  real number from `0` to `2`
- `depth` — how many reads the sample's call rests on
- `quality` — how confident the caller is in that call

A sample **passes** when its `depth` is at least `min_depth` and its `quality`
is at least `min_quality`.

Report two numbers over the passing samples:

- `AC` — the sum of their `dosage` values
- `AN` — two per passing sample

## Two gates

`make test` checks the answer against `cases/`.

`make vec` checks how the program got it. It runs the same build on the
fixture that `vec.mk` names and single-steps the call to `solve`: every
instruction `solve` retires, in its own code, in the functions it calls, and in
the library routines those call, except the Go runtime's stack growth, heap
growth, and preemption. It passes when `solve` retires fewer than one scalar
instruction per sample, averaged over the fixture, and at least one packed SIMD
instruction per 50 samples. Scalar instructions are

- scalar floating-point arithmetic, compares, and conversions; loads and stores
  of 64 bits or less that do not address the stack; and moves of one lane from
  a vector register into a general-purpose one, wherever they run;
- arithmetic, compares, bit operations, and conditional sets and moves on
  general-purpose registers, except in loop iterations that load several
  elements into a vector register at once.

String instructions such as `rep movsb` do not count.

A `solve` that gets every case right but does its work on the samples one at
a time in scalar registers fails `make vec`.

`make vec` grades the code the compiler chose for `x86-64-v3`, so it refuses
inline or standalone assembly, a `#pragma`, a `target` or `optimize` attribute,
Rust's `#[target_feature]`, `#[naked]`, and `build.rs`, and cgo, and it stops at
the first AVX-512 instruction the program itself runs. It needs Linux, `ptrace`,
and `objdump`.

Both gates must pass. There are no large cases and no timing gate: `make bench`
has nothing to run here.

## Constraints

- `0 ≤ n ≤ 200000`, where `dosage`, `depth`, and `quality` all have length `n`
- every `dosage` is a multiple of `1/4096` from `0` to `2`
- `0 ≤ depth ≤ 10^6` and `0 ≤ quality ≤ 10^6`
- `0 ≤ min_depth ≤ 10^6` and `0 ≤ min_quality ≤ 10^6`

## Input

```json
{"dosage":[1.5,0.25,2],"depth":[30,8,44],"quality":[99,50,15],"min_depth":10,"min_quality":20}
```

## Output

One line: `AC` written with exactly twelve digits after the decimal point, a
single space, then `AN`.

```
1.500000000000 2
```

## Examples

**Example 1** — the second sample is under the depth floor, the third under the quality floor
```
{"dosage":[1.5,0.25,2],"depth":[30,8,44],"quality":[99,50,15],"min_depth":10,"min_quality":20} → 1.500000000000 2
```

**Example 2** — a sample sitting exactly on both thresholds passes; one read short does not
```
{"dosage":[0.0009765625,2],"depth":[10,9],"quality":[20,20],"min_depth":10,"min_quality":20} → 0.000976562500 2
```

**Example 3** — no sample passes
```
{"dosage":[1,2,0.5],"depth":[5,30,12],"quality":[99,10,60],"min_depth":20,"min_quality":20} → 0.000000000000 0
```

## Run

From the challenge directory:

```
make -C c test
make -C c vec
make -C rust test
make -C rust vec
make -C go test
make -C go vec
```

All three solver directories build for `x86-64-v3`, the target `make vec`
grades, and `make test` compiles with the same flags, so both need a machine
with AVX2, BMI2, and FMA.

The Go solver directory builds with `GOEXPERIMENT=simd`, so a Go `solve` may
import `simd/archsimd`. Its `go.mod` requires Go 1.27.1 or newer.

> No debug prints. Extra stdout breaks the test harness and signals you don't
> have a mental model yet. Build the model, then write the code.

Stuck? See `hints/01.md`.

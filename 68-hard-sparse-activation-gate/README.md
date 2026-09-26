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

`make vec` checks how the program got it. It runs the same build on the
fixture that `vec.mk` names and single-steps the call to `solve`: every
instruction `solve` retires, in its own code, in the functions it calls, and in
the library routines those call, except the Go runtime's stack growth, heap
growth, and preemption. It passes when `solve` retires fewer than one scalar
instruction per score, averaged over the fixture, and at least one packed SIMD
instruction per 50 scores. Scalar instructions are

- scalar floating-point arithmetic, compares, and conversions; loads and stores
  of 64 bits or less that do not address the stack; and moves of one lane from
  a vector register into a general-purpose one, wherever they run;
- arithmetic, compares, bit operations, and conditional sets and moves on
  general-purpose registers, except in loop iterations that load several
  elements into a vector register at once.

String instructions such as `rep movsb` do not count.

`make vec` grades the code the compiler chose for `x86-64-v3`, so it refuses
inline or standalone assembly, a `#pragma`, a `target` or `optimize` attribute,
Rust's `#[target_feature]`, `#[naked]`, and `build.rs`, and cgo, and it stops at
the first AVX-512 instruction the program itself runs. `solve` must run on one
thread: `make vec` stops when it starts a thread, a process, or a goroutine. It
needs Linux, `ptrace`, and `objdump`.

Both gates must pass. There are no large cases and no timing gate: `make bench`
has nothing to run here.

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

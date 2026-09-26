# 17 — Medium — 0/1 Knapsack

**Task**: Pack a bag of capacity W to maximise total value, taking each item at most once.

**Difficulty**: medium
**Time estimate**: ~40 min

## Problem

You're packing a bag with capacity `W`. Each item has a weight and a value, and
you may take each item at most once (no splitting an item, no taking it twice).
Maximise the total value of the packed items without letting their combined
weight exceed `W`.

Constraints: items up to 1000, capacity up to 10⁴, and each weight is a positive
signed 32-bit integer. Values fit in signed 32-bit integers. The result and all
accumulated values must fit in a signed 64-bit integer.

## Input

```json
{"capacity": 10, "items": [{"weight":5,"value":10},{"weight":4,"value":40},{"weight":6,"value":30},{"weight":3,"value":50}]}
```

## Output

A single signed 64-bit integer: the maximum achievable total value.

## Examples

**Example 1** — four items with different weights and values
```
capacity 10, items above → 90   (weight 4+3, value 40+50)
```

**Example 2**
```
{"capacity":10,"items":[{"weight":6,"value":10},{"weight":5,"value":6},{"weight":5,"value":6}]} → 12
```

## Run

```
make -C rust
make -C go
make -C c
make -C python
```

Stuck? See `hints/01.md`.

## Level 3 — `make vec`

Optional, in C, Rust, and Go:

```
make -C c vec
make -C rust vec
make -C go vec
```

`make vec` builds its own `x86-64-v3` program, checks it on every case in
`cases/`, then single-steps the call to `solve` on the fixture that `vec.mk`
names: every instruction `solve` retires, in its own code, in the functions it
calls, and in the library routines those call, except the Go runtime's stack
growth, heap growth, and preemption. It passes when `solve` retires fewer than
one scalar instruction per item-capacity pair, averaged over the fixture, and at
least one packed SIMD instruction per 50 pairs; an input with `n` items has
`n × capacity` pairs. Scalar instructions are

- scalar floating-point arithmetic, compares, and conversions; loads and stores
  of 64 bits or less that do not address the stack; and moves of one lane from
  a vector register into a general-purpose one, wherever they run;
- arithmetic, compares, bit operations, and conditional sets and moves on
  general-purpose registers, except in loop iterations that load several
  elements into a vector register at once.

String instructions such as `rep movsb` do not count.

`make vec` grades the code the compiler chose, so it refuses inline or
standalone assembly, a `#pragma`, a `target` or `optimize` attribute, Rust's
`#[target_feature]`, `#[naked]`, `build.rs`, and cgo, and it stops at the first
AVX-512 instruction the program itself runs. It needs Linux, `ptrace`,
`objdump`, and a CPU with AVX2, BMI2, and FMA. `make test` and `make bench` keep
their own builds, and a `solve` must pass them too. The Go directory builds with
`GOEXPERIMENT=simd`, so `solve` may import `simd/archsimd`; its `go.mod`
requires Go 1.27.1 or newer.

Stuck on this level? See `hints/04.md`.

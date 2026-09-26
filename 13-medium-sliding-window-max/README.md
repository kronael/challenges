# 13 — Medium — Sliding Window Maximum

**Task**: Report the maximum sensor reading in every consecutive window of k readings.

**Difficulty**: medium
**Time estimate**: ~30 min

## Problem

Given a stream of sensor readings and a window size `k`, a window of `k`
consecutive readings slides from the far left of the stream to the far right,
moving one position at a time. For each position, report the maximum reading
visible in the window. The first window covers readings `0..k-1`; the last
covers the final `k` readings. There are `n - k + 1` windows in all.

The stream may be long, and the number of windows can be large. Your program
must produce every requested maximum within the stated limits.

Constraints: `n` up to 10⁶, `1 ≤ k ≤ n`, readings fit in a signed 32-bit
integer.

## Input

```json
{"k": 3, "arr": [1, 3, -1, -3, 5, 3, 6, 7]}
```

## Output

The maximum of each window, in order, space-separated.

## Examples

**Example 1**
```
k=3, arr [1,3,-1,-3,5,3,6,7] → 3 3 5 5 6 7
```

**Example 2**
```
k=2, arr [9,1,1,1] → 9 1 1
```

## Run

```
make -C rust
make -C go
make -C c
make -C python
```

The C, Rust, and Go directories build every target for `x86-64-v3`: C at
`-O3 -march=x86-64-v3`, Rust in release with `-C target-cpu=x86-64-v3`, and Go
with `GOAMD64=v3`. Every target there needs a machine with AVX2, BMI2, and FMA.

Stuck? See `hints/01.md`.

## Level 3 — `make vec`

`make test` checks the answer and `make bench` its speed. `make vec`, the
optional third level, checks how the program got it. After confirming the
answer on every case in `cases/`, it runs the program on the fixture that
`vec.mk` names and single-steps the call to `solve`: every instruction `solve`
retires, in its own code, in the functions it calls, and in the library
routines those call, except the Go runtime's stack growth, heap growth, and
preemption. It passes when `solve` retires fewer than one scalar instruction
per reading, averaged over the fixture, and at least one packed SIMD
instruction per 50 readings. Scalar instructions are

- scalar floating-point arithmetic, compares, and conversions; loads and stores
  of 64 bits or less that do not address the stack; and moves of one lane from
  a vector register into a general-purpose one, wherever they run;
- arithmetic, compares, bit operations, and conditional sets and moves on
  general-purpose registers, except in loop iterations that load several
  elements into a vector register at once.

String instructions such as `rep movsb` do not count.

A `solve` that gets every case right but does its work on the readings one
at a time in scalar registers fails `make vec`.

`make vec` grades the code the compiler chose for `x86-64-v3`, so it refuses
inline or standalone assembly, a `#pragma`, a `target` or `optimize` attribute,
Rust's `#[target_feature]`, `#[naked]`, and `build.rs`, and cgo, and it stops at
the first AVX-512 instruction the program itself runs. `solve` must run on one
thread: `make vec` stops when it starts a thread, a process, or a goroutine. It
needs Linux, `ptrace`, and `objdump`.

The C, Rust, and Go directories have this level; the Python one does not:

```
make -C c vec
make -C rust vec
make -C go vec
```

`make vec` grades the same `x86-64-v3` program that `make test` and
`make bench` check. The Go directory builds every target with
`GOEXPERIMENT=simd`, so a Go `solve` may import `simd/archsimd`; its `go.mod`
requires Go 1.27.1 or newer.

Stuck on this level? See `hints/05.md`.

Source: https://leetcode.com/problems/sliding-window-maximum/

# 46 — Hard — CRISPR Off-Targets

**Task**: For each CRISPR guide sequence, count the genome windows that pass a
simplified mismatch-only candidate-site rule.

**Difficulty**: hard
**Time estimate**: ~45 min

## Problem

A CRISPR guide is represented as a DNA sequence of length `L` over the alphabet
`{A, C, G, T}`. The challenge uses Hamming distance, the number of positions at
which two equal-length strings differ, as a simplified candidate-site rule.

The model does not check PAM compatibility, the opposite DNA strand, DNA or RNA
bulges, mismatch position effects, or measured cleavage activity. It also has no
coordinate for the intended site, so it cannot distinguish that site from other
exact matches. The reported values are candidate counts, not predictions of
biological binding or cleavage.

You are given a genome string, a guide length `L`, a mismatch budget `d`, and a
list of guides, each of length `L`. A length-`L` window is a candidate for a
guide when their Hamming distance is at most `d`. For each guide, count all such
windows. Windows overlap: every starting offset from `0` through
`|genome| - L` is separate, and one window may count for several guides. If the
genome is shorter than `L`, it has no windows and every guide's count is zero.

Constraints: genome length up to `10⁶`; `L` in `8 … 20`; up to `2·10³` guides;
`d` in `0 … 4`; alphabet `{A, C, G, T}`.

## Input

```json
{"d": 1, "len": 8, "genome": "ACGTACGTGGACGTACGA", "guides": ["ACGTACGT", "TTTTTTTT"]}
```

## Output

Space-separated integers, one per guide, in input order: the candidate-site
count for each guide. When there are no guides, the line is empty.

## Examples

**Example 1** — `ACGTACGT` matches window 0 exactly and window 10 (`ACGTACGA`)
with one mismatch, so 2; `TTTTTTTT` is too far from every window, so 0
```
{"d":1,"len":8,"genome":"ACGTACGTGGACGTACGA","guides":["ACGTACGT","TTTTTTTT"]} → 2 0
```

**Example 2** — with `d=0` only exact-match windows count; a 10-base poly-A
genome has 3 length-8 windows, all `AAAAAAAA`
```
{"d":0,"len":8,"genome":"AAAAAAAAAA","guides":["AAAAAAAA"]} → 3
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
per base of `genome`, averaged over the fixture, and at least one packed SIMD
instruction per 50 bases. Scalar instructions are

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

The C, Rust, and Go directories have this level; the Python one does not:

```
make -C c vec
make -C rust vec
make -C go vec
```

`make vec` grades the same `x86-64-v3` program that `make test` and
`make bench` check. A `solve` may use x86 SIMD intrinsics: `<immintrin.h>` in
C, `std::arch::x86_64` in Rust, and `simd/archsimd` in Go. In Rust, a call to
one of them is `unsafe` outside a `#[target_feature]` function, and `make vec`
refuses `#[target_feature]`, so a Rust `solve` makes those calls in an `unsafe`
block. The Go directory builds every target with `GOEXPERIMENT=simd`, which
`simd/archsimd` needs; its `go.mod` requires Go 1.27.1 or newer.

Stuck on this level? See `hints/05.md`.

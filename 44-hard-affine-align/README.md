# 44 — Hard — Affine Alignment Score

**Task**: Given two protein strings `s` and `t`, compute the maximum score of a
global end-to-end alignment under the BLOSUM62 substitution matrix with affine
gap penalties.

**Difficulty**: hard
**Time estimate**: ~40 min

## Problem

An *alignment* of `s` and `t` writes the two strings one above the other, left to
right in their original order, inserting gap symbols (`-`) into either string so
that both end up the same length. Every column then holds either two residues
(amino acids, one from each string) or one residue and a gap. A *global* alignment must cover
both strings end to end — every residue of `s` and of `t` appears in some column.

Each column is scored, and the alignment's score is the sum over all columns:

- A column with two residues `a` and `b` scores `BLOSUM62[a][b]` — the
  substitution score from the BLOSUM62 matrix (reproduced below).
- A maximal run of `L` consecutive gaps in one string (a single insertion or
  deletion of length `L`) costs `gap_open + gap_extend·(L−1)`, with
  `gap_open = 11` and `gap_extend = 1`. So a length-1 gap costs 11, length-2
  costs 12, length-3 costs 13, and so on. This cost is *subtracted* from the
  score. "Affine" means opening a gap is expensive but extending an already-open
  gap is cheap, so one long gap is preferred over several short ones.

Report the maximum achievable alignment score over all valid global alignments.

Both strings use the 20 standard amino acids `ARNDCQEGHILKMFPSTWYV`.

Constraints: `1 ≤ |s|, |t| ≤ 2500`; both strings over the 20 standard amino
acids; the score fits in a signed 32-bit integer.

### BLOSUM62

Rows and columns are indexed by `ARNDCQEGHILKMFPSTWYV` (in that order).

```
    A  R  N  D  C  Q  E  G  H  I  L  K  M  F  P  S  T  W  Y  V
A   4 -1 -2 -2  0 -1 -1  0 -2 -1 -1 -1 -1 -2 -1  1  0 -3 -2  0
R  -1  5  0 -2 -3  1  0 -2  0 -3 -2  2 -1 -3 -2 -1 -1 -3 -2 -3
N  -2  0  6  1 -3  0  0  0  1 -3 -3  0 -2 -3 -2  1  0 -4 -2 -3
D  -2 -2  1  6 -3  0  2 -1 -1 -3 -4 -1 -3 -3 -1  0 -1 -4 -3 -3
C   0 -3 -3 -3  9 -3 -4 -3 -3 -1 -1 -3 -1 -2 -3 -1 -1 -2 -2 -1
Q  -1  1  0  0 -3  5  2 -2  0 -3 -2  1  0 -3 -1  0 -1 -2 -1 -2
E  -1  0  0  2 -4  2  5 -2  0 -3 -3  1 -2 -3 -1  0 -1 -3 -2 -2
G   0 -2  0 -1 -3 -2 -2  6 -2 -4 -4 -2 -3 -3 -2  0 -2 -2 -3 -3
H  -2  0  1 -1 -3  0  0 -2  8 -3 -3 -1 -2 -1 -2 -1 -2 -2  2 -3
I  -1 -3 -3 -3 -1 -3 -3 -4 -3  4  2 -3  1  0 -3 -2 -1 -3 -1  3
L  -1 -2 -3 -4 -1 -2 -3 -4 -3  2  4 -2  2  0 -3 -2 -1 -2 -1  1
K  -1  2  0 -1 -3  1  1 -2 -1 -3 -2  5 -1 -3 -1  0 -1 -3 -2 -2
M  -1 -1 -2 -3 -1  0 -2 -3 -2  1  2 -1  5  0 -2 -1 -1 -1 -1  1
F  -2 -3 -3 -3 -2 -3 -3 -3 -1  0  0 -3  0  6 -4 -2 -2  1  3 -1
P  -1 -2 -2 -1 -3 -1 -1 -2 -2 -3 -3 -1 -2 -4  7 -1 -1 -4 -3 -2
S   1 -1  1  0 -1  0  0  0 -1 -2 -2  0 -1 -2 -1  4  1 -3 -2 -2
T   0 -1  0 -1 -1 -1 -1 -2 -2 -1 -1 -1 -1 -2 -1  1  5 -2 -2  0
W  -3 -3 -4 -4 -2 -2 -3 -2 -2 -3 -2 -3 -1  1 -4 -3 -2 11  2 -3
Y  -2 -2 -2 -3 -2 -1 -2 -3  2 -1 -1 -2 -1  3 -3 -2 -2  2  7 -1
V   0 -3 -3 -3 -1 -2 -2 -3 -3  3  1 -2  1 -1 -2 -2  0 -3 -1  4
```

## Input

```json
{"s": "PRTEINS", "t": "PRTWPSEIN"}
```

## Output

A single integer: the maximum global alignment score.

## Examples

**Example 1** — from the source problem
```
{"s":"PRTEINS","t":"PRTWPSEIN"} → 8
```

**Example 2** — identical strings align on the diagonal with no gaps
```
{"s":"MEEPQSDPSV","t":"MEEPQSDPSV"} → 52
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
preemption. It passes when, on that fixture, `solve` retires fewer than
`|s|·|t|` scalar instructions and at least `|s|·|t| / 50` packed SIMD
instructions. Scalar instructions are

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

Stuck on this level? See `hints/06.md`.

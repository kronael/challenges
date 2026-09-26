# 67 — Medium — Tick Frame Audit

**Task**: Given a fixed-width tick feed and its frame layout, report how many
frames follow the layout and how many bytes sit where the layout does not
allow them.

**Difficulty**: medium
**Time estimate**: ~30 min

## Problem

A market-data feed delivers ticks as fixed-width text records. Every record — a
**frame** — is exactly `width` bytes. Offsets inside a frame count from 0, and
the layout gives each offset one required class:

- offset `width − 1` holds the **terminator**, the byte `\n`
- each offset listed in `separators` holds a **separator**, the byte `|`
- every other offset holds **payload**: any allowed byte except `|` and `\n`

`stream` is the feed as received. Its length is a multiple of `width`, and
frame `k` occupies bytes `k·width` through `(k+1)·width − 1`. The feed can
arrive corrupted, so any allowed byte can appear at any offset.

A byte is a **stray** when it is not what its offset requires: a separator or
terminator offset holding any other byte, or a payload offset holding `|` or
`\n`. A frame is **clean** when none of its bytes is a stray.

Report two numbers:

- `clean` — how many frames are clean
- `stray` — how many stray bytes the whole stream holds

## Two gates

`make test` checks the answer against `cases/`.

`make vec` checks how the program got it. It runs the same build on the
fixture that `vec.mk` names and single-steps the call to `solve`: every
instruction `solve` retires, in its own code, in the functions it calls, and in
the library routines those call, except the Go runtime's stack growth, heap
growth, and preemption. It passes when `solve` retires fewer than one scalar
instruction per byte of `stream`, averaged over the fixture, and at least one
packed SIMD instruction per 50 bytes. Scalar instructions are

- scalar floating-point arithmetic, compares, and conversions; loads and stores
  of 64 bits or less that do not address the stack; and moves of one lane from
  a vector register into a general-purpose one, wherever they run;
- arithmetic, compares, bit operations, and conditional sets and moves on
  general-purpose registers, except in loop iterations that load several
  elements into a vector register at once.

String instructions such as `rep movsb` do not count.

A `solve` that gets every case right but does its work on the bytes one at
a time in scalar registers fails `make vec`.

`make vec` grades the code the compiler chose for `x86-64-v3`, so it refuses
inline or standalone assembly, a `#pragma`, a `target` or `optimize` attribute,
Rust's `#[target_feature]`, `#[naked]`, and `build.rs`, and cgo, and it stops at
the first AVX-512 instruction the program itself runs. It needs Linux, `ptrace`,
and `objdump`.

Both gates must pass. There are no large cases and no timing gate: `make bench`
has nothing to run here.

## Constraints

- `32 ≤ width ≤ 1024`
- `separators` is strictly increasing, each entry in `[0, width − 2]`; it may
  be empty
- `0 ≤ len(stream) ≤ 2^20`, and `len(stream)` is a multiple of `width`
- every byte of `stream` is printable ASCII (`0x20`–`0x7E`) or `\n` (`0x0A`)

## Input

```json
{"width":32,"separators":[4,15,22],"stream":"AAPL|0000187.25|000300|00000017\nMSFT|0000411.10|001200|00000018\n"}
```

`stream` is a JSON string. Its `\n`, `\"`, and `\\` escapes decode to the
single bytes they name, and the decoded bytes are the feed.

## Output

One line: `clean`, a single space, `stray`.

```
2 0
```

## Examples

**Example 1** — two frames that follow the layout
```
{"width":32,"separators":[4,15,22],"stream":"AAPL|0000187.25|000300|00000017\nMSFT|0000411.10|001200|00000018\n"} → 2 0
```

**Example 2** — the second frame lacks a separator; the third has a stray pipe and newline
```
{"width":32,"separators":[4,15,22],"stream":"AAPL|0000187.25|000300|00000017\nMSFT|0000411.10 001200|00000018\nGOOG|00|0174.50|000050|000\n0019\n"} → 1 3
```

**Example 3** — the newline arrives a byte early, so the payload and the terminator are both wrong
```
{"width":32,"separators":[4,15,22],"stream":"NVDA|0000121.75|000900|0000002\nX"} → 0 2
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

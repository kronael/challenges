# 67 — Medium — Tick Frame Audit

**Task**: Given a fixed-width tick feed and its record layout, report how many
records follow the layout and how many bytes sit where the layout does not
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

`make vec` checks the shape of the code that produced it. It compiles `solve`
for `x86-64-v3` at `-O3` and reads back the loops the compiler emitted: one of
them must carry the whole arithmetic of the audit in packed SIMD lanes. A
`solve` whose loops the compiler leaves in scalar registers fails `make vec`
even when every case passes.

Both gates must pass. There are no large cases and no timing gate — this
challenge is graded on the code the compiler emits, not on elapsed time.
`make bench` has no recipes to generate here and says so.

## Constraints

- `1 ≤ width ≤ 1024`
- `separators` is strictly increasing, each entry in `[0, width − 2]`; it may
  be empty
- `0 ≤ len(stream) ≤ 2^20`, and `len(stream)` is a multiple of `width`
- every byte of `stream` is printable ASCII (`0x20`–`0x7E`) or `\n` (`0x0A`)
- `clean` and `stray` both fit in a signed 32-bit integer

## Input

```json
{"width":13,"separators":[4,9],"stream":"AAPL|1234|56\nMSFT|0078|12\n"}
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
{"width":13,"separators":[4,9],"stream":"AAPL|1234|56\nMSFT|0078|12\n"} → 2 0
```

**Example 2** — a separator missing from the second frame; a pipe and a newline inside the third frame's payload
```
{"width":13,"separators":[4,9],"stream":"AAPL|1234|56\nMSFT 0078|12\nGO|G|00\n1|3X\n"} → 1 3
```

**Example 3** — with `width` 1 there is no room for a separator, and every byte is its own frame
```
{"width":1,"separators":[],"stream":"\n\n|\n"} → 3 1
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

The C and Go solver directories build for `x86-64-v3`, the same target
`make vec` grades, so running `make test` needs a machine with AVX2.

The Go solver directory builds with `GOEXPERIMENT=simd`, so a Go `solve` may
import `simd/archsimd`. Its `go.mod` requires Go 1.27.1 or newer.

> No debug prints. Extra stdout breaks the test harness and signals you don't
> have a mental model yet. Build the model, then write the code.

Stuck? See `HINTS.md`.

# 46 — Hard — CRISPR Off-Targets

**Task**: For each CRISPR guide sequence, count how many places in a genome it could bind by mistake — every length-`L` window of the genome that differs from the guide in at most `d` positions.

**Difficulty**: hard
**Time estimate**: ~45 min

## Problem

A CRISPR guide is a short DNA sequence of length `L` over the alphabet
`{A, C, G, T}`. It is designed to bind one intended site, but it will also bind
*off-target* sites that are close enough — anywhere in the genome that matches
the guide in all but a few bases. "Close enough" is measured by **Hamming
distance**: the number of positions at which two equal-length strings differ.

You are given a genome string, a guide length `L`, a mismatch budget `d`, and a
list of guides (each of length `L`). A length-`L` window of the genome is an
*off-target* of a guide if its Hamming distance to that guide is at most `d`.
For **each** guide, output how many of the genome's length-`L` windows are
off-targets. Windows overlap: every starting offset `0 … |genome|−L` is its own
window, and the same window can be an off-target of several guides.

Constraints: genome length up to `2·10⁵`; `L` in `8 … 20`; up to `10³` guides;
`d` in `0 … 4`; alphabet `{A, C, G, T}`.

## Input

```json
{"d": 1, "len": 8, "genome": "ACGTACGTGGACGTACGA", "guides": ["ACGTACGT", "TTTTTTTT"]}
```

## Output

Space-separated integers, one per guide, in input order: the off-target count
for each guide.

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
cd rust   && make
cd go     && make
cd python && make
```

Stuck? See `HINTS.md`.

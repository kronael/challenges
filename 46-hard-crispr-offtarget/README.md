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

Constraints: genome length up to `2·10⁵`; `L` in `8 … 20`; up to `10³` guides;
`d` in `0 … 4`; alphabet `{A, C, G, T}`.

## Input

```json
{"d": 1, "len": 8, "genome": "ACGTACGTGGACGTACGA", "guides": ["ACGTACGT", "TTTTTTTT"]}
```

## Output

Space-separated integers, one per guide, in input order: the candidate-site
count for each guide.

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
make -C python
```

Stuck? See `HINTS.md`.

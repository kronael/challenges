# 45 — Hard — K-mer Assembly

**Task**: Given the shuffled, complete multiset of length-`k` substrings from one
DNA string, reconstruct that string.

**Difficulty**: hard
**Time estimate**: ~40 min

## Problem

The input is an error-free, complete *k-mer multiset* from one linear DNA
string. It contains the length-`k` substring at every starting offset, including
repeated copies when the same substring occurs more than once. The k-mers arrive
in arbitrary order. For `GGCTTACCA` and `k = 4`, the multiset contains `GGCT`,
`GCTT`, `CTTA`, `TTAC`, `TACC`, and `ACCA`.

Rebuild the single DNA string that produced the multiset. Consecutive k-mers in
that string overlap in exactly `k - 1` characters. The answer therefore has
`number of k-mers + k - 1` characters.

The input is guaranteed to admit exactly one such linear reconstruction, so the
answer is unique.

Constraints: `2 ≤ k ≤ 32`; `1 ≤ number of k-mers ≤ 2·10⁵`; every k-mer has
length `k` and uses only `A`, `C`, `G`, `T`; a unique linear reconstruction is
guaranteed.

## Input

```json
{"k": 4, "kmers": ["CTTA", "ACCA", "TACC", "GGCT", "GCTT", "TTAC"]}
```

## Output

A single DNA string on one line — the reconstructed molecule.

## Examples

**Example 1** — the six 4-mers tile `GGCTTACCA`
```
{"k":4,"kmers":["CTTA","ACCA","TACC","GGCT","GCTT","TTAC"]} → GGCTTACCA
```

**Example 2** — a single k-mer is already the whole string
```
{"k":3,"kmers":["ACG"]} → ACG
```

## Run

```
make -C rust
make -C go
make -C python
```

Stuck? See `HINTS.md`.

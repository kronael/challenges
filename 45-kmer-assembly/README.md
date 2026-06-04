# 45 — K-mer Assembly

**Task**: Given the shuffled multiset of all length-`k` fragments that tile one
DNA molecule, reconstruct the original DNA string.

**Difficulty**: medium
**Time estimate**: ~40 min

## Problem

A sequencing machine reads one contiguous DNA molecule and reports every
length-`k` substring (a *k-mer*) it contains — with multiplicity, but in
arbitrary order. If the molecule is `GGCTTACCA` and `k = 4`, the reported k-mers
are the six windows `GGCT`, `GCTT`, `CTTA`, `TTAC`, `TACC`, `ACCA`, shuffled.

Your job is the inverse: given the shuffled multiset of k-mers, rebuild the
single DNA string they came from. The fragments tile the molecule so that each
consecutive pair overlaps in exactly `k - 1` characters — the last `k - 1`
letters of one fragment are the first `k - 1` letters of the next. Stitching the
fragments back along those overlaps spells the original string, which is
`(number of k-mers) + k - 1` letters long.

The input is guaranteed to admit exactly one such linear reconstruction, so the
answer is unique.

The collection is large — up to `2·10⁵` k-mers. The obvious approach — for each
fragment, scan all the others to find the one whose first `k - 1` letters match
this fragment's last `k - 1` letters — is quadratic and will not finish in time
at that scale; part of the challenge is finding a formulation that does.

Constraints: `2 ≤ k ≤ 32`; up to `2·10⁵` k-mers; alphabet `{A, C, G, T}`;
a unique reconstruction is guaranteed.

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
cd rust   && make
cd go     && make
cd python && make
```

Stuck? See `HINTS.md`.

Source: https://rosalind.info/problems/pcov/ (Compeau, Pevzner & Tesler,
*Nature Biotechnology* 2011)

# 48 — Shortest Superstring

**Task**: Reassemble a chromosome from its sequencing reads — output the shortest DNA string that contains every read as a substring.

**Difficulty**: medium
**Time estimate**: ~40 min

## Problem

A linear chromosome was sequenced into a set of overlapping `reads` (short DNA
strings over `ACGT`). The reads came from one strand, in unknown order, and every
adjacent pair in the true layout overlaps by **more than half** the length of a
read: the suffix of one read is exactly the prefix of the next, and that shared
stretch is longer than half the read. Under this guarantee the chromosome has a
single shortest reconstruction.

Output that reconstruction: the shortest string that contains all reads as
substrings. With the >half-length-overlap promise it is exactly the chromosome the
reads were cut from, and it is unique.

The input is large — up to about `2·10⁴` reads, each up to ~1 kbp. The obvious
approach of scoring the overlap of *every* pair of reads and re-scanning the
survivors round after round is too slow at that scale: comparing all pairs is
already quadratic in the number of reads, and recomputing it as the assembly grows
pushes it well past what finishes in time. Part of the challenge is assembling the
chromosome without ever building that full all-pairs overlap table.

Constraints: up to `2·10⁴` reads; each read up to ~1000 bp; alphabet `ACGT`;
adjacent true neighbours overlap by strictly more than half a read length; the
reconstruction is unique.

## Input

```json
{"reads": ["ATTAGACCTG", "CCTGCCGGAA", "AGACCTGCCG", "GCCGGAATAC"]}
```

## Output

A single DNA string: the reassembled chromosome.

## Examples

**Example 1** — the four reads chain through their overlaps into one sequence
```
{"reads":["ATTAGACCTG","CCTGCCGGAA","AGACCTGCCG","GCCGGAATAC"]} → ATTAGACCTGCCGGAATAC
```

**Example 2** — a single read is already the whole chromosome
```
{"reads":["GATTACA"]} → GATTACA
```

## Run

```
cd rust   && make
cd go     && make
cd python && make
```

Stuck? See `HINTS.md`.

Source: Rosalind — Genome Assembly as Shortest Superstring (https://rosalind.info/problems/long/)

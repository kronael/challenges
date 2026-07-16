# 48 — Hard — Shortest Superstring

**Task**: Reassemble a chromosome from its sequencing reads — output the shortest DNA string that contains every read as a substring.

**Difficulty**: hard
**Time estimate**: ~40 min

## Problem

A linear chromosome was sequenced into a collection of reads over `A`, `C`, `G`,
and `T`. The reads came from one strand and arrive in unknown order. Repeated
copies of a read count as one substring requirement. A read contained in another
read is already covered and adds no placement requirement.

After duplicate and contained reads are removed, the remaining reads form one
chain. The chain has one head and one tail. Every other read has exactly one
predecessor and one successor. For each adjacent pair, a proper suffix of the
first read equals a prefix of the second and has length strictly greater than
half the length of both reads. No other ordered pair has such an overlap. These
conditions guarantee one reconstruction.

Output the unique shortest string that contains every input read as a substring.

Constraints: `0 ≤ number of reads ≤ 2·10⁴`; each read has `1` to `1000`
characters from `A`, `C`, `G`, `T`; the reduced collection satisfies the chain
promise above.

## Input

```json
{"reads": ["ATTAGACCTG", "CCTGCCGGAA", "AGACCTGCCG", "GCCGGAATAC"]}
```

## Output

A single DNA string: the reassembled chromosome. For an empty read collection,
print an empty line.

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
make -C rust
make -C go
make -C python
```

Stuck? See `HINTS.md`.

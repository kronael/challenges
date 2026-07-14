# 53 — Hard — Circular Genome Distance

**Task**: Find the fewest allowed rearrangements needed to transform one
circular genome into another.

**Difficulty**: hard
**Time estimate**: ~90 min

## Problem

A genome is a collection of circular chromosomes. Each chromosome is a signed
sequence of synteny blocks. The sign records the block's orientation. Across a
genome, every block from `1` through `n` appears exactly once.

One rearrangement cuts two adjacencies and reconnects the four exposed ends in
one of the other pairings. Find the minimum number of rearrangements needed to
transform genome `a` into genome `b`.

The two genomes contain the same blocks. Chromosome order and circular rotation
do not matter. A chromosome may also be read in the opposite direction if every
block sign is reversed.

Constraints: `1 <= n <= 200000` and at most `n` chromosomes per genome.

## Input

```json
{"a":[[1,-2,-3,4]],"b":[[1,2,-4,-3]]}
```

## Output

Print the minimum number of rearrangements as one integer.

## Example

```text
{"a":[[1,2,3,4]],"b":[[1,2,3,4]]} → 0
```

## Run

```bash
cd python && make
cd go     && make
cd rust   && make
```

Stuck? See `HINTS.md`.

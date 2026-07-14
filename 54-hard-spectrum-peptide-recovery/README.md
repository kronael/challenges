# 54 — Hard — Spectrum Peptide Recovery

**Task**: Recover a cyclic peptide from its exact mass spectrum.

**Difficulty**: hard
**Time estimate**: ~90 min

## Problem

A cyclic peptide is represented by the integer masses of its amino acids. Its
theoretical spectrum contains the mass of every contiguous fragment around the
cycle, including `0` and the full peptide mass. Equal-mass fragments appear
with their full multiplicity.

Given an allowed mass alphabet and a sorted theoretical spectrum, recover a
peptide whose spectrum matches exactly. Several rotations or different peptides
may match. Print the lexicographically smallest mass sequence among all matches.
Print `NONE` if no peptide matches.

Constraints: 1 to 18 allowed masses, parent mass at most 2000, and at most 20
amino acids in any matching peptide.

## Input

```json
{"masses":[113,128,186],"spectrum":[0,113,128,186,241,299,314,427]}
```

## Output

Print the chosen masses separated by spaces, or `NONE`.

## Example

```text
113 128 186
```

## Run

```bash
cd python && make
cd go     && make
cd rust   && make
```

Stuck? See `HINTS.md`.

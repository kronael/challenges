# 54 — Hard — Spectrum Peptide Recovery

**Task**: Recover a cyclic peptide from an idealized integer mass spectrum, if
one exists.

**Difficulty**: hard
**Time estimate**: ~90 min

## Problem

A non-empty cyclic peptide is represented by the integer masses of its amino
acids. For a peptide with `r` masses and total mass `P`, its spectrum contains:

- `0` exactly once;
- `P` exactly once;
- for every start position and every fragment length from `1` through `r - 1`,
  the sum of that many consecutive masses around the cycle.

Each start position and fragment length contributes one entry, even when
several fragments have the same mass. Multiplicity therefore matters. A peptide
of length `r` has `r·(r - 1) + 2` spectrum entries.

Given an allowed mass alphabet and a sorted candidate mass multiset, recover a
peptide whose spectrum matches it exactly. The candidate may be unrealizable.
Several rotations or different peptides may match. Print the lexicographically
smallest mass sequence among all matches. Print `NONE` if no peptide matches.

Constraints: `masses` contains `1` to `18` distinct positive integers;
`spectrum` is a nondecreasing list of at least two nonnegative integers, starts
with `0`, and ends with a positive parent mass at most `2000`; any matching
peptide has at most `20` masses.

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
make -C python
make -C go
make -C rust
```

Stuck? See `HINTS.md`.

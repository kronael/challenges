# 44 — Hard — Affine Alignment Score

**Task**: Given two protein strings `s` and `t`, compute the maximum score of a
global end-to-end alignment under the BLOSUM62 substitution matrix with affine
gap penalties.

**Difficulty**: hard
**Time estimate**: ~40 min

## Problem

An *alignment* of `s` and `t` writes the two strings one above the other, left to
right in their original order, inserting gap symbols (`-`) into either string so
that both end up the same length. Every column then holds either two residues
(one from each string) or one residue and a gap. A *global* alignment must cover
both strings end to end — every residue of `s` and of `t` appears in some column.

Each column is scored, and the alignment's score is the sum over all columns:

- A column with two residues `a` and `b` scores `BLOSUM62[a][b]` — the
  substitution score from the BLOSUM62 matrix (reproduced below).
- A maximal run of `L` consecutive gaps in one string (a single insertion or
  deletion of length `L`) costs `gap_open + gap_extend·(L−1)`, with
  `gap_open = 11` and `gap_extend = 1`. So a length-1 gap costs 11, length-2
  costs 12, length-3 costs 13, and so on. This cost is *subtracted* from the
  score. "Affine" means opening a gap is expensive but extending an already-open
  gap is cheap, so one long gap is preferred over several short ones.

Report the maximum achievable alignment score over all valid global alignments.

Both strings use the 20 standard amino acids `ARNDCQEGHILKMFPSTWYV`.

Constraints: `1 ≤ |s|, |t| ≤ 2000`; both strings over the 20 standard amino
acids; the score fits in a signed 32-bit integer.

### BLOSUM62

Rows and columns are indexed by `ARNDCQEGHILKMFPSTWYV` (in that order).

```
    A  R  N  D  C  Q  E  G  H  I  L  K  M  F  P  S  T  W  Y  V
A   4 -1 -2 -2  0 -1 -1  0 -2 -1 -1 -1 -1 -2 -1  1  0 -3 -2  0
R  -1  5  0 -2 -3  1  0 -2  0 -3 -2  2 -1 -3 -2 -1 -1 -3 -2 -3
N  -2  0  6  1 -3  0  0  0  1 -3 -3  0 -2 -3 -2  1  0 -4 -2 -3
D  -2 -2  1  6 -3  0  2 -1 -1 -3 -4 -1 -3 -3 -1  0 -1 -4 -3 -3
C   0 -3 -3 -3  9 -3 -4 -3 -3 -1 -1 -3 -1 -2 -3 -1 -1 -2 -2 -1
Q  -1  1  0  0 -3  5  2 -2  0 -3 -2  1  0 -3 -1  0 -1 -2 -1 -2
E  -1  0  0  2 -4  2  5 -2  0 -3 -3  1 -2 -3 -1  0 -1 -3 -2 -2
G   0 -2  0 -1 -3 -2 -2  6 -2 -4 -4 -2 -3 -3 -2  0 -2 -2 -3 -3
H  -2  0  1 -1 -3  0  0 -2  8 -3 -3 -1 -2 -1 -2 -1 -2 -2  2 -3
I  -1 -3 -3 -3 -1 -3 -3 -4 -3  4  2 -3  1  0 -3 -2 -1 -3 -1  3
L  -1 -2 -3 -4 -1 -2 -3 -4 -3  2  4 -2  2  0 -3 -2 -1 -2 -1  1
K  -1  2  0 -1 -3  1  1 -2 -1 -3 -2  5 -1 -3 -1  0 -1 -3 -2 -2
M  -1 -1 -2 -3 -1  0 -2 -3 -2  1  2 -1  5  0 -2 -1 -1 -1 -1  1
F  -2 -3 -3 -3 -2 -3 -3 -3 -1  0  0 -3  0  6 -4 -2 -2  1  3 -1
P  -1 -2 -2 -1 -3 -1 -1 -2 -2 -3 -3 -1 -2 -4  7 -1 -1 -4 -3 -2
S   1 -1  1  0 -1  0  0  0 -1 -2 -2  0 -1 -2 -1  4  1 -3 -2 -2
T   0 -1  0 -1 -1 -1 -1 -2 -2 -1 -1 -1 -1 -2 -1  1  5 -2 -2  0
W  -3 -3 -4 -4 -2 -2 -3 -2 -2 -3 -2 -3 -1  1 -4 -3 -2 11  2 -3
Y  -2 -2 -2 -3 -2 -1 -2 -3  2 -1 -1 -2 -1  3 -3 -2 -2  2  7 -1
V   0 -3 -3 -3 -1 -2 -2 -3 -3  3  1 -2  1 -1 -2 -2  0 -3 -1  4
```

## Input

```json
{"s": "PRTEINS", "t": "PRTWPSEIN"}
```

## Output

A single integer: the maximum global alignment score.

## Examples

**Example 1** — from the source problem
```
{"s":"PRTEINS","t":"PRTWPSEIN"} → 8
```

**Example 2** — identical strings align on the diagonal with no gaps
```
{"s":"MEEPQSDPSV","t":"MEEPQSDPSV"} → 52
```

## Run

```
cd rust   && make
cd go     && make
cd python && make
```

Stuck? See `HINTS.md`.

Source: https://rosalind.info/problems/gaff/

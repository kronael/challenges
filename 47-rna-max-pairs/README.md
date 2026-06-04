# 47 — RNA Max Pairs

**Task**: Given an RNA strand, choose the largest possible set of base pairs that fold the strand back on itself without any pair crossing another.

**Difficulty**: medium
**Time estimate**: ~40 min

## Problem

An RNA molecule is a string over the alphabet `A`, `C`, `G`, `U`. It folds by
forming *base pairs* between positions. You must choose a set of pairs that is as
large as possible, subject to these rules:

- **Allowed partners.** A position holding `A` may pair only with `U`, and `C`
  only with `G` (in either direction): the allowed unordered pairs are `A–U` and
  `C–G`. If `allow_wobble` is true, the wobble pair `G–U` is also allowed. No
  other combination may pair.
- **Each base used once.** A position may belong to at most one pair.
- **No crossing.** Pairs must nest, never cross. If `(i, j)` and `(k, l)` are both
  chosen pairs with `i < k`, then either `i < k < l < j` (one nested inside the
  other) or `i < j < k < l` (one entirely before the other). The interleaved case
  `i < k < j < l` is forbidden.
- **Minimum loop length.** A pair `(i, j)` with `i < j` is only allowed when
  `j - i > min_loop`; that is, at least `min_loop` unpaired positions would sit
  between the two paired bases. With `min_loop = 0`, adjacent positions may pair.

Output the maximum number of pairs achievable.

The strand can be up to 400 bases long. Enumerating fold choices position by
position branches exponentially and will not finish at that scale; the challenge
is to find a formulation that does.

Constraints: `1 ≤ len(rna) ≤ 400`; the alphabet is exactly `A`, `C`, `G`, `U`;
`0 ≤ min_loop`; `allow_wobble` is a boolean.

## Input

```json
{"rna": "AUGCUA", "min_loop": 0, "allow_wobble": false}
```

## Output

A single integer: the maximum number of non-crossing base pairs.

## Examples

**Example 1** — `A·U`, `U·A`, and `G·C` can all be formed without crossing
```
{"rna":"AUGCUA","min_loop":0,"allow_wobble":false} → 3
```

**Example 2** — no two bases here can pair under the rules
```
{"rna":"AAAA","min_loop":0,"allow_wobble":false} → 0
```

## Run

```
cd rust   && make
cd go     && make
cd python && make
```

Stuck? See `HINTS.md`.

Source: Nussinov et al., "Algorithms for loop matchings" (1978),
https://pubmed.ncbi.nlm.nih.gov/6161375/

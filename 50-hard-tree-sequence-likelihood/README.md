# 50 — Hard — Tree Sequence Likelihood

Compute the natural logarithm of the probability of DNA sequences observed at
the leaves of a rooted evolutionary tree.

Each site evolves independently. The root starts in `A`, `C`, `G`, or `T`
according to `prior`. Along every tree edge, `transition[x][y]` is the
probability that parent base `x` produces child base `y`. Internal-node bases
are unknown and must all contribute to the final probability.

## Input

```json
{
  "parent": [-1, 0, 0],
  "sequences": [null, "A", "G"],
  "prior": [0.25, 0.25, 0.25, 0.25],
  "transition": [
    [0.94, 0.02, 0.02, 0.02],
    [0.02, 0.94, 0.02, 0.02],
    [0.02, 0.02, 0.94, 0.02],
    [0.02, 0.02, 0.02, 0.94]
  ]
}
```

Node `0` is the root. For every other node `i`, `parent[i] < i`. A `null`
sequence marks an internal node. Every leaf has a DNA string, and all leaf
strings have the same non-zero length. Matrix rows and columns use `A`, `C`,
`G`, `T` order.

Constraints: `3 ≤ nodes ≤ 255`; every internal node has at least two children;
all probabilities are positive finite decimals; `prior` and every transition
row sum to one within `10⁻⁹`; `nodes · sequence_length ≤ 2,000,000`.

## Output

Print the total natural-log likelihood across all sites, rounded to exactly six
digits after the decimal point.

## Example

```text
{"parent":[-1,0,0],"sequences":[null,"A","G"],"prior":[0.25,0.25,0.25,0.25],"transition":[[0.94,0.02,0.02,0.02],[0.02,0.94,0.02,0.02],[0.02,0.02,0.94,0.02],[0.02,0.02,0.02,0.94]]}
→ -4.645992
```

## Run

```text
cd rust   && make
cd go     && make
cd python && make
```

Stuck? See `HINTS.md`.

# Hints — 32 Relational Programming

> Spoilers. Open only when stuck.

- **Relational, not functional**: the same predicate that *checks* a split also
  *generates* all of them; one definition runs forward and backward. This is the
  way `append(X, Y, [1,2,3])` in Prolog runs backward to produce every
  prefix/suffix split — you describe what a solution looks like and let the engine
  search.
- **CSP for constraint satisfaction**: declare variables, their domains, and the
  constraints with the [`python-constraint`](https://pypi.org/project/python-constraint/)
  library (`pip install python-constraint`), then ask for `getSolutions()` instead
  of looping and pruning by hand. Build a `Problem()`, `addVariable(name, domain)`
  for each variable, `addConstraint(predicate, [vars])` for each rule, and read off
  every model.
- **N-Queens**: one variable per row, domain `0..n-1` (the column). Add an
  `AllDifferentConstraint()` so no two share a column, and a pairwise constraint
  `abs(col[r1] - col[r2]) != abs(r1 - r2)` so no two share a diagonal. Each
  returned solution is the dict of row → column; pack it into a tuple ordered by
  row.
- **Graph coloring**: one variable per node, domain `0..k-1`. For every edge
  `(u, v)` add the constraint `color[u] != color[v]`. `getSolutions()` is the full
  list of proper colorings; an impossible instance (e.g. K4 with 3 colors) returns
  an empty list with no special-casing.
- **SEND + MORE = MONEY**: variables `S E N D M O R Y`, domain `0..9`,
  `AllDifferentConstraint()`. Forbid leading zeros by giving `S` and `M` the domain
  `1..9` (or adding `!= 0` constraints). Add the single arithmetic constraint that
  the place-value sum holds: `1000*S + 100*E + 10*N + D + 1000*M + 100*O + 10*R + E
  == 10000*M + 1000*O + 100*N + 10*E + Y`.
- **enumerate_splits**: no constraint solver needed — this is the relational
  `append`. Every split is `(lst[:i], lst[i:])` for `i` in `0..len(lst)`
  inclusive, so the empty list still yields the one pair `([], [])`. A list
  comprehension over `range(len(lst) + 1)` is the whole thing.

# 32 — Relational Programming in Python

A Prolog program defines **relations**, not functions. `append(X, Y, [1,2,3])`
runs *backward*: it enumerates every way to split `[1,2,3]` into a prefix `X` and
suffix `Y`. The same clause that *checks* a split also *generates* all of them.
That is the shift: you describe **what a solution looks like** — its constraints —
and let the engine find every assignment that satisfies them. You never write the
search.

## The tools

- [`python-constraint`](https://pypi.org/project/python-constraint/) — declare
  variables, domains, and constraints; ask for `getSolutions()`.
- `itertools` / `functools` — relational enumeration when a CSP is overkill.

## The prompt

For each `solve_*`, **state the constraints, then enumerate solutions** — do not
hand-code a backtracking search. The test of relational thinking: your N-Queens
must say "no two queens share a column, row, or diagonal" and ask for all models,
not loop-and-prune. Your splits must read like `append(X, Y, lst)` — every
`(prefix, suffix)` pair — not an index walk you reasoned about.

If you find yourself writing nested `for` loops with `if`-guards and an
accumulator, you are thinking imperatively. Declare the relation instead.

## Run

```
cd python && make test
```

Source: relational/logic programming (Prolog); `python-constraint`, SEND+MORE=MONEY.

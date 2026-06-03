# 32 — Relational Programming

Solve N-Queens, graph coloring, SEND+MORE=MONEY, and list splits by *declaring constraints and enumerating models* — never by writing a backtracking loop.
Hard because the mental shift is real: you must describe *what a solution looks like* and let the engine search, the way `append(X, Y, [1,2,3])` in Prolog runs backward to generate every prefix/suffix split.

## Teaches

- **Relational, not functional**: the same predicate that *checks* a split also *generates* all of them; one definition runs forward and backward.
- **CSP for constraint satisfaction**: declare variables, domains, and constraints with `python-constraint`, then ask for `getSolutions()` instead of looping and pruning by hand.

## Run
```
cd python && make
```
Source: relational/logic programming (Prolog); [`python-constraint`](https://pypi.org/project/python-constraint/)

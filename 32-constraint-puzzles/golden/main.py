from constraint import AllDifferentConstraint, Problem


def solve_nqueens(n: int) -> list[tuple[int, ...]]:
    """Return ALL solutions to the N-Queens problem as tuples of column positions.

    Each solution is a tuple where index = row, value = column, with no two queens
    sharing a column or diagonal. n=4 has 2 solutions, n=8 has 92.
    """
    if n == 0:
        return [()]
    p = Problem()
    p.addVariables(range(n), range(n))
    p.addConstraint(AllDifferentConstraint())
    for r1 in range(n):
        for r2 in range(r1 + 1, n):
            p.addConstraint(lambda c1, c2, d=r2 - r1: abs(c1 - c2) != d, (r1, r2))
    return [tuple(sol[r] for r in range(n)) for sol in p.getSolutions()]


def solve_graph_coloring(
    n: int, edges: list[tuple[int, int]], k: int
) -> list[dict[int, int]]:
    """Return ALL valid k-colorings of the graph with n nodes and given edges.

    Each solution maps node -> color in 0..k-1, with adjacent nodes differing.
    """
    p = Problem()
    p.addVariables(range(n), range(k))
    for u, v in edges:
        p.addConstraint(lambda a, b: a != b, (u, v))
    return p.getSolutions()


def solve_send_more_money() -> list[dict[str, int]]:
    """Return ALL assignments of distinct digits to SEND + MORE = MONEY."""
    p = Problem()
    p.addVariables("ENDORY", range(10))
    p.addVariables("SM", range(1, 10))
    p.addConstraint(AllDifferentConstraint())
    p.addConstraint(
        lambda s, e, n, d, m, o, r, y: (
            (1000 * s + 100 * e + 10 * n + d) + (1000 * m + 100 * o + 10 * r + e)
            == 10000 * m + 1000 * o + 100 * n + 10 * e + y
        ),
        "SENDMORY",
    )
    return p.getSolutions()


def enumerate_splits(lst: list) -> list[tuple[list, list]]:
    """Return ALL ways to split lst into a (prefix, suffix) pair.

    The relational append: ([], lst) through (lst, []) at every cut point.
    """
    return [(lst[:i], lst[i:]) for i in range(len(lst) + 1)]

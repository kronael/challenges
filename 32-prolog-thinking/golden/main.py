def solve_nqueens(n: int) -> list[tuple[int, ...]]:
    """Return ALL solutions to the N-Queens problem as tuples of column positions.

    Each solution is a tuple where index = row, value = column. Think relationally:
    one variable per row, domain 0..n-1, constrain "no two share a column or
    diagonal", then ask for every model. Do not write a backtracking loop.
    """
    pass


def solve_graph_coloring(
    n: int, edges: list[tuple[int, int]], k: int
) -> list[dict[int, int]]:
    """Return ALL valid k-colorings of graph with n nodes and given edges.

    One variable per node, domain 0..k-1, constrain "adjacent nodes differ".
    Each solution maps node -> color.
    """
    pass


def solve_send_more_money() -> list[dict[str, int]]:
    """Return ALL assignments of digits to SEND + MORE = MONEY.

    Variables S,E,N,D,M,O,R,Y over 0..9, all different, leading digits nonzero,
    and the arithmetic relation holds. Describe the relation; enumerate solutions.
    """
    pass


def enumerate_splits(lst: list) -> list[tuple[list, list]]:
    """Return ALL ways to split lst into (prefix, suffix). Think: append(X, Y, lst).

    For [1,2,3] that is ([],[1,2,3]), ([1],[2,3]), ([1,2],[3]), ([1,2,3],[]):
    every split point, not an index walk you reasoned about by hand.
    """
    pass

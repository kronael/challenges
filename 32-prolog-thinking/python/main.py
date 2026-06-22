def solve_nqueens(n: int) -> list[tuple[int, ...]]:
    """Return ALL solutions to the N-Queens problem as tuples of column positions.

    Each solution is a tuple where index = row, value = column, so that no two
    queens share a column or a diagonal. n=4 has 2 solutions, n=8 has 92.
    """
    pass


def solve_graph_coloring(
    n: int, edges: list[tuple[int, int]], k: int
) -> list[dict[int, int]]:
    """Return ALL valid k-colorings of the graph with n nodes and given edges.

    Each solution maps node -> color in 0..k-1, with adjacent nodes differing.
    An impossible instance returns an empty list.
    """
    pass


def solve_send_more_money() -> list[dict[str, int]]:
    """Return ALL assignments of distinct digits to SEND + MORE = MONEY.

    Letters S,E,N,D,M,O,R,Y map to distinct digits 0..9, S and M are nonzero,
    and the addition holds. Each solution maps letter -> digit. There is one.
    """
    pass


def enumerate_splits(lst: list) -> list[tuple[list, list]]:
    """Return ALL ways to split lst into a (prefix, suffix) pair.

    For [1, 2, 3]: ([], [1,2,3]), ([1], [2,3]), ([1,2], [3]), ([1,2,3], []).
    For []: the single pair ([], []).
    """
    pass

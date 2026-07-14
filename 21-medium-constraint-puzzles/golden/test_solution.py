from main import (
    enumerate_splits,
    solve_graph_coloring,
    solve_nqueens,
    solve_send_more_money,
)


def _is_valid_queens(sol, n):
    if not isinstance(sol, tuple):
        return False
    if len(sol) != n:
        return False
    if any(not isinstance(col, int) or col < 0 or col >= n for col in sol):
        return False
    if len(set(sol)) != n:
        return False
    for r1 in range(n):
        for r2 in range(r1 + 1, n):
            if abs(sol[r1] - sol[r2]) == abs(r1 - r2):
                return False
    return True


def test_nqueens_zero_has_empty_board_solution():
    assert solve_nqueens(0) == [()]


def test_nqueens_4_has_two_solutions():
    sols = solve_nqueens(4)
    assert len(sols) == 2
    assert len(set(sols)) == 2
    assert all(_is_valid_queens(sol, 4) for sol in sols)


def test_nqueens_8_has_92_solutions():
    sols = solve_nqueens(8)
    assert len(sols) == 92
    assert len(set(sols)) == 92
    assert all(_is_valid_queens(sol, 8) for sol in sols)


def test_triangle_three_coloring_has_six():
    edges = [(0, 1), (1, 2), (0, 2)]
    sols = solve_graph_coloring(3, edges, 3)
    assert len(sols) == 6
    for coloring in sols:
        assert set(coloring) == {0, 1, 2}
        assert all(0 <= color <= 2 for color in coloring.values())
        assert all(coloring[u] != coloring[v] for u, v in edges)


def test_isolated_nodes_are_still_colored():
    sols = solve_graph_coloring(3, [], 2)
    assert len(sols) == 8
    assert all(set(coloring) == {0, 1, 2} for coloring in sols)


def test_k4_three_coloring_impossible():
    edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    assert solve_graph_coloring(4, edges, 3) == []


def test_send_more_money_unique():
    sols = solve_send_more_money()
    assert sols == [{"S": 9, "E": 5, "N": 6, "D": 7, "M": 1, "O": 0, "R": 8, "Y": 2}]


def test_enumerate_splits():
    assert enumerate_splits([1, 2, 3]) == [
        ([], [1, 2, 3]),
        ([1], [2, 3]),
        ([1, 2], [3]),
        ([1, 2, 3], []),
    ]
    assert enumerate_splits([]) == [([], [])]

import inspect

from solution import (
    enumerate_splits,
    solve_graph_coloring,
    solve_nqueens,
    solve_send_more_money,
)

# these must use python-constraint or itertools.combinations, not nested loops.
# the paradigm under test is relational: declare constraints + enumerate models.


def _is_valid_queens(sol, n):
    if sorted(sol) != list(range(n)) and len(set(sol)) != n:
        # columns need not be a permutation a priori, but no two may collide
        pass
    for r1 in range(n):
        for r2 in range(r1 + 1, n):
            if sol[r1] == sol[r2]:
                return False
            if abs(sol[r1] - sol[r2]) == abs(r1 - r2):
                return False
    return True


def test_nqueens_4_has_two_solutions():
    sols = solve_nqueens(4)
    assert len(sols) == 2
    for s in sols:
        assert len(s) == 4
        assert _is_valid_queens(s, 4)
    assert len(set(sols)) == 2


def test_nqueens_8_has_92_solutions():
    sols = solve_nqueens(8)
    assert len(sols) == 92
    for s in sols:
        assert _is_valid_queens(s, 8)
    assert len(set(sols)) == 92


def test_triangle_three_coloring_has_six():
    edges = [(0, 1), (1, 2), (0, 2)]
    sols = solve_graph_coloring(3, edges, 3)
    assert len(sols) == 6
    for c in sols:
        for u, v in edges:
            assert c[u] != c[v]


def test_k4_three_coloring_impossible():
    edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    assert solve_graph_coloring(4, edges, 3) == []


def test_send_more_money_unique():
    sols = solve_send_more_money()
    assert len(sols) == 1
    assert sols[0] == {"S": 9, "E": 5, "N": 6, "D": 7, "M": 1, "O": 0, "R": 8, "Y": 2}


def test_enumerate_splits():
    assert enumerate_splits([1, 2, 3]) == [
        ([], [1, 2, 3]),
        ([1], [2, 3]),
        ([1, 2], [3]),
        ([1, 2, 3], []),
    ]
    assert enumerate_splits([]) == [([], [])]


def test_relational_not_imperative():
    # The prompt: solutions describe constraints, they do not hand-roll search.
    # A relational solve_nqueens leans on python-constraint; enumerate_splits
    # leans on slicing/itertools. Reject solutions that bury a manual nested
    # backtracking loop (cheap heuristic: source must reference the declared
    # tooling rather than only raw control flow).
    src = inspect.getsource(solve_nqueens) + inspect.getsource(solve_graph_coloring)
    assert "constraint" in src.lower(), "use python-constraint, not a hand-coded search"

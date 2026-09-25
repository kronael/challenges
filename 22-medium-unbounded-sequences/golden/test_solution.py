import inspect
from itertools import islice

import main


def test_scaffold_exports_expected_functions():
    for name in [
        "naturals",
        "sieve",
        "primes",
        "fibonacci",
        "running_average",
        "collatz",
        "zipWith",
        "unfold",
    ]:
        assert callable(getattr(main, name))


def test_scaffold_signatures_match_readme():
    assert str(inspect.signature(main.naturals)) == "(start: int = 0) -> Iterator[int]"
    assert (
        str(inspect.signature(main.sieve)) == "(nums: Iterator[int]) -> Iterator[int]"
    )
    assert str(inspect.signature(main.primes)) == "() -> Iterator[int]"
    assert str(inspect.signature(main.fibonacci)) == "() -> Iterator[int]"
    assert (
        str(inspect.signature(main.running_average))
        == "(nums: Iterator[float]) -> Iterator[float]"
    )
    assert str(inspect.signature(main.collatz)) == "(n: int) -> Iterator[int]"
    assert (
        str(inspect.signature(main.zipWith))
        == "(f, xs: Iterator, ys: Iterator) -> Iterator"
    )
    assert str(inspect.signature(main.unfold)) == "(f, seed)"


def test_naturals_from_default_and_offset():
    assert list(islice(main.naturals(), 5)) == [0, 1, 2, 3, 4]
    assert list(islice(main.naturals(5), 5)) == [5, 6, 7, 8, 9]


def test_primes_first_eight():
    assert list(islice(main.primes(), 8)) == [2, 3, 5, 7, 11, 13, 17, 19]


def test_sieve_keeps_only_primes_from_stream():
    assert list(islice(main.sieve(main.naturals(2)), 6)) == [2, 3, 5, 7, 11, 13]
    assert list(main.sieve(iter([2, 3, 4, 5, 6, 7, 8, 9]))) == [2, 3, 5, 7]


def test_fibonacci_first_ten():
    assert list(islice(main.fibonacci(), 10)) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]


def test_running_average_is_prefix_mean():
    assert list(islice(main.running_average(main.naturals(1)), 4)) == [
        1.0,
        1.5,
        2.0,
        2.5,
    ]


def test_collatz_continues_past_one():
    # 6 -> 3 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1, then the 1,4,2,1 cycle.
    assert list(islice(main.collatz(6), 12)) == [6, 3, 10, 5, 16, 8, 4, 2, 1, 4, 2, 1]


def test_zipwith_combines_two_streams():
    got = main.zipWith(lambda a, b: a + b, main.naturals(0), main.naturals(10))
    assert list(islice(got, 4)) == [10, 12, 14, 16]


def test_unfold_stops_on_none():
    countdown = main.unfold(lambda s: None if s == 0 else (s, s - 1), 3)
    assert list(countdown) == [3, 2, 1]
    assert list(main.unfold(lambda s: None, 42)) == []

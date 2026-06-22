import inspect

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

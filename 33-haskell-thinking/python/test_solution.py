import time
from itertools import islice

from main import (
    collatz,
    fibonacci,
    naturals,
    primes,
    running_average,
    sieve,
    unfold,
    zipWith,
)


def test_naturals():
    assert list(islice(naturals(), 5)) == [0, 1, 2, 3, 4]
    assert list(islice(naturals(1), 5)) == [1, 2, 3, 4, 5]


def test_primes():
    assert list(islice(primes(), 10)) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]


def test_sieve_directly():
    assert list(islice(sieve(naturals(2)), 6)) == [2, 3, 5, 7, 11, 13]


def test_fibonacci():
    assert list(islice(fibonacci(), 10)) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]


def test_running_average():
    avg = running_average(iter([1, 3, 5, 7]))
    assert list(avg) == [1.0, 2.0, 3.0, 4.0]


def test_running_average_from_infinite_stream():
    assert list(islice(running_average(naturals(1)), 4)) == [1.0, 1.5, 2.0, 2.5]


def test_collatz():
    assert list(islice(collatz(6), 8)) == [6, 3, 10, 5, 16, 8, 4, 2]
    assert list(islice(collatz(1), 6)) == [1, 4, 2, 1, 4, 2]


def test_zipwith():
    s = zipWith(lambda a, b: a + b, naturals(1), naturals(1))
    assert list(islice(s, 5)) == [2, 4, 6, 8, 10]


def test_unfold():
    s = unfold(lambda n: (n, n * 2) if n < 100 else None, 1)
    assert list(s) == [1, 2, 4, 8, 16, 32, 64]


def test_unfold_can_be_infinite():
    s = unfold(lambda n: (n, n + 1), 3)
    assert list(islice(s, 5)) == [3, 4, 5, 6, 7]


def test_primes_is_lazy():
    # CRITICAL: primes() must be an infinite generator, not a materialised list.
    # next() returns 2 in O(1) — no precomputation, no upper bound chosen up front.
    g = primes()
    t0 = time.perf_counter()
    assert next(g) == 2
    assert time.perf_counter() - t0 < 0.1
    # A pipeline of generators stays usable without ever exhausting it.
    assert next(g) == 3
    assert list(islice(g, 3)) == [5, 7, 11]

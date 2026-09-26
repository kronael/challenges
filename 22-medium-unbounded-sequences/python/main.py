from typing import Iterator  # noqa: UP035 -- signature contract pins typing.Iterator


def naturals(start: int = 0) -> Iterator[int]:
    """Infinite generator of naturals from start: start, start+1, start+2, ..."""


def sieve(nums: Iterator[int]) -> Iterator[int]:
    """Given an ascending stream of ints >= 2, yield the primes among them, in order."""


def primes() -> Iterator[int]:
    """Infinite generator of primes: 2, 3, 5, 7, 11, ..."""


def fibonacci() -> Iterator[int]:
    """Infinite Fibonacci sequence: 0, 1, 1, 2, 3, 5, 8, ..."""


def running_average(nums: Iterator[float]) -> Iterator[float]:
    """Infinite generator of prefix averages, one output per input. No list accumulation."""


def collatz(n: int) -> Iterator[int]:
    """Infinite Collatz sequence from n (continues past 1 into the 1, 4, 2, 1, ... cycle)."""


def zipWith(f, xs: Iterator, ys: Iterator) -> Iterator:
    """Apply f element-wise to two (possibly infinite) sequences (Haskell zipWith)."""


def unfold(f, seed):
    """Haskell unfoldr: f(state) -> (value, next_state) to continue, or None to stop."""

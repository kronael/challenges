from typing import Iterator  # noqa: UP035 -- signature contract pins typing.Iterator


def naturals(start: int = 0) -> Iterator[int]:
    """Infinite generator of naturals from start: start, start+1, start+2, ..."""
    n = start
    while True:
        yield n
        n += 1


def sieve(nums: Iterator[int]) -> Iterator[int]:
    """Given an ascending stream of ints >= 2, yield the primes among them, in order."""
    known = []
    for n in nums:
        if all(n % p for p in known):
            known.append(n)
            yield n


def primes() -> Iterator[int]:
    """Infinite generator of primes: 2, 3, 5, 7, 11, ..."""
    return sieve(naturals(2))


def fibonacci() -> Iterator[int]:
    """Infinite Fibonacci sequence: 0, 1, 1, 2, 3, 5, 8, ..."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def running_average(nums: Iterator[float]) -> Iterator[float]:
    """Infinite generator of prefix averages, one output per input. No list accumulation."""
    total = 0.0
    for count, n in enumerate(nums, start=1):
        total += n
        yield total / count


def collatz(n: int) -> Iterator[int]:
    """Infinite Collatz sequence from n (continues past 1 into the 1, 4, 2, 1, ... cycle)."""
    while True:
        yield n
        n = n // 2 if n % 2 == 0 else 3 * n + 1


def zipWith(f, xs: Iterator, ys: Iterator) -> Iterator:
    """Apply f element-wise to two infinite sequences (Haskell zipWith)."""
    for x, y in zip(xs, ys):
        yield f(x, y)


def unfold(f, seed):
    """Haskell unfoldr: f(state) -> (value, next_state) to continue, or None to stop."""
    state = seed
    while True:
        result = f(state)
        if result is None:
            return
        value, state = result
        yield value

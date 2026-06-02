from typing import Iterator


def naturals(start: int = 0) -> Iterator[int]:
    """Infinite generator of naturals from start.

    Haskell: [start..]. Yield forever; the consumer decides how far.
    """
    pass


def sieve(nums: Iterator[int]) -> Iterator[int]:
    """Sieve of Eratosthenes as a lazy generator pipeline.

    Take the first element p (prime), yield it, then sieve the rest with every
    multiple of p filtered out. Corecursive: define the stream, do not loop to N.
    """
    pass


def primes() -> Iterator[int]:
    """Infinite generator of primes. Uses sieve(naturals(2))."""
    pass


def fibonacci() -> Iterator[int]:
    """Infinite Fibonacci sequence: 0, 1, 1, 2, 3, 5, 8, ..."""
    pass


def running_average(nums: Iterator[float]) -> Iterator[float]:
    """Infinite generator of running averages. No list accumulation.

    Carry (count, total) as state and yield total/count for each input. A scan,
    not a slice-and-divide.
    """
    pass


def collatz(n: int) -> Iterator[int]:
    """Infinite Collatz sequence from n (terminates at 1,4,2,1,4,2,... cycle)."""
    pass


def zipWith(f, xs: Iterator, ys: Iterator) -> Iterator:
    """Apply f element-wise to two infinite sequences (Haskell zipWith)."""
    pass


def unfold(f, seed):
    """Haskell unfoldr: generate sequence from seed by applying f repeatedly.

    f(state) -> (value, next_state) | None to stop.
    """
    pass

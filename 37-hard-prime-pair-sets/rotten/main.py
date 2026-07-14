import json
import sys
from itertools import combinations


def is_prime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def concat_ok(a, b):
    return is_prime(int(f"{a}{b}")) and is_prime(int(f"{b}{a}"))


def solve(size=5, limit=10000):
    if size <= 0:
        return 0

    primes = [value for value in range(2, limit) if is_prime(value)]
    best = None
    # Naive: inspect all C(pi(limit), size) groups and recheck every pair by
    # trial division. Correct, but the combinatorial scan TIMEOUTs on large cases.
    for group in combinations(primes, size):
        if all(concat_ok(a, b) for a, b in combinations(group, 2)):
            total = sum(group)
            if best is None or total < best:
                best = total
    return -1 if best is None else best


def main():
    data = json.load(sys.stdin)
    print(solve(data.get("size", 5), data.get("limit", 10000)))


if __name__ == "__main__":
    main()

import json
import sys


def is_prime(n):
    # Naive trial division: correct, but death on the 8-digit concatenations — the trap.
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def concat_ok(a, b):
    return is_prime(int(f"{a}{b}")) and is_prime(int(f"{b}{a}"))


def solve(size=5):
    if size <= 0:
        return 0

    limit = 10000
    sieve = bytearray([1]) * limit
    sieve[0] = sieve[1] = 0
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            sieve[i * i :: i] = bytearray(len(sieve[i * i :: i]))
    primes = [i for i in range(2, limit) if sieve[i]]

    compat = {}

    def ok(a, b):
        key = (a, b) if a < b else (b, a)
        v = compat.get(key)
        if v is None:
            v = concat_ok(a, b)
            compat[key] = v
        return v

    best = [float("inf")]

    def extend(group, group_sum, start):
        if len(group) == size:
            if group_sum < best[0]:
                best[0] = group_sum
            return
        need = size - len(group)
        for idx in range(start, len(primes)):
            p = primes[idx]
            if group_sum + p * need >= best[0]:
                break
            if all(ok(p, q) for q in group):
                extend(group + [p], group_sum + p, idx + 1)

    extend([], 0, 0)
    return best[0]


def main():
    data = json.load(sys.stdin)
    print(solve(data.get("size", 5)))


if __name__ == "__main__":
    main()

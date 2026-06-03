import json
import sys


def is_prime(n):
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def concat_ok(a, b):
    return is_prime(int(f"{a}{b}")) and is_prime(int(f"{b}{a}"))


def solve():
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
        if len(group) == 5:
            if group_sum < best[0]:
                best[0] = group_sum
            return
        need = 5 - len(group)
        for idx in range(start, len(primes)):
            p = primes[idx]
            if group_sum + p * need >= best[0]:
                break
            if all(ok(p, q) for q in group):
                extend(group + [p], group_sum + p, idx + 1)

    extend([], 0, 0)
    return best[0]


def main():
    json.load(sys.stdin)
    print(solve())


if __name__ == "__main__":
    main()

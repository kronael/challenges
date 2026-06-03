import json
import sys


def solve(n):
    if n <= 2:
        return 0
    # sieve odd numbers only: index i represents value 2*i+1
    size = n // 2  # covers odds 1,3,5,...,< n (excludes n itself)
    sieve = bytearray([1]) * size
    sieve[0] = 0  # value 1 is not prime
    i = 1
    while (2 * i + 1) * (2 * i + 1) < n:
        if sieve[i]:
            p = 2 * i + 1
            start = (p * p - 1) // 2
            sieve[start::p] = bytearray(len(range(start, size, p)))
        i += 1
    return 1 + sum(sieve)  # +1 for the prime 2


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["n"]))


if __name__ == "__main__":
    main()

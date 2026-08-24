import json
import sys


def solve(n, target, exposures):
    # Naive: build all 2^n baskets and keep the closest total. Every basket is
    # summed from scratch over the positions it holds, so the scan is
    # O(2^n * n) and shares nothing between one basket and the next. Fine on the
    # small cases; at n = 38 that is 275 billion baskets, so both large cases
    # TIMEOUT.
    best = abs(target)
    for basket in range(1 << n):
        total = sum(exposures[i] for i in range(n) if basket >> i & 1)
        gap = abs(total - target)
        if gap < best:
            best = gap
    return best


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["n"], obj["target"], obj["exposures"]))


if __name__ == "__main__":
    main()

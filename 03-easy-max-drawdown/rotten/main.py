import json
import sys


def solve(prices):
    # Naive O(n^2): compare every earlier day against every later day —
    # correct, but TIMEOUTs on the large cases (the trap).
    n = len(prices)
    best = 0
    for i in range(n):
        for j in range(i + 1, n):
            d = prices[i] - prices[j]
            if d > best:
                best = d
    return best


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["prices"]))


if __name__ == "__main__":
    main()

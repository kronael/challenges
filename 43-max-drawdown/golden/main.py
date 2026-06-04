import json
import sys


def solve(prices):
    peak = -(1 << 62)
    best = 0
    for x in prices:
        if x > peak:
            peak = x
        elif peak - x > best:
            best = peak - x
    return best


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["prices"]))


if __name__ == "__main__":
    main()

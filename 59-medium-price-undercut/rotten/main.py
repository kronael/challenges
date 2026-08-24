import json
import sys


def solve(n, prices):
    # Naive O(n^2): for every day, walk the rest of the series until a strictly
    # lower settlement shows up. A series that keeps rising never offers an early
    # exit, so the walks add up to n(n-1)/2 comparisons — correct on the small
    # cases, TIMEOUT on the large ones.
    out = []
    for i in range(n):
        wait = 0
        for j in range(i + 1, n):
            if prices[j] < prices[i]:
                wait = j - i
                break
        out.append(wait)
    return out


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["n"], obj["prices"]))


if __name__ == "__main__":
    main()

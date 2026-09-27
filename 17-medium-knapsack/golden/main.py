import json
import sys


def solve(capacity, items):
    dp = [0] * (capacity + 1)
    for it in items:
        w, v = it["weight"], it["value"]
        for c in range(capacity, w - 1, -1):
            cand = dp[c - w] + v
            if cand > dp[c]:
                dp[c] = cand
    return dp[capacity]


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["capacity"], obj["items"]))


if __name__ == "__main__":
    main()

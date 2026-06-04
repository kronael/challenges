import json
import sys


def solve(intervals):
    # Naive O(n^2) DP: sort by end, then for each interval scan ALL earlier ones
    # to find the best compatible predecessor. Correct, but TIMEOUTs on large n — the trap.
    ivs = sorted(intervals, key=lambda iv: iv[1])
    n = len(ivs)
    if n == 0:
        return 0
    dp = [1] * n
    for i in range(n):
        for j in range(i):
            if ivs[j][1] <= ivs[i][0] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
    return max(dp)


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["intervals"]))


if __name__ == "__main__":
    main()

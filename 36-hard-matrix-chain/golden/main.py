import json
import sys


def solve(dims):
    n = len(dims) - 1
    if n <= 1:
        return 0
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            best = float("inf")
            for k in range(i, j):
                cost = dp[i][k] + dp[k + 1][j] + dims[i] * dims[k + 1] * dims[j + 1]
                if cost < best:
                    best = cost
            dp[i][j] = best
    return dp[0][n - 1]


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["dims"]))


if __name__ == "__main__":
    main()

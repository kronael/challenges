import json
import sys


def solve(k, pages):
    # Naive O(k * n^2) DP over split points: correct, but TIMEOUTs on the large
    # cases — the trap. dp[j][i] = min achievable largest block when splitting the
    # prefix pages[:i] into at most j contiguous blocks.
    n = len(pages)
    if n == 0:
        return 0
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + pages[i]

    INF = float("inf")
    # one block: the whole prefix sum
    dp = [prefix[i] for i in range(n + 1)]
    for _ in range(1, k):
        ndp = [INF] * (n + 1)
        for i in range(1, n + 1):
            best = INF
            for s in range(0, i):
                cand = max(dp[s], prefix[i] - prefix[s])
                if cand < best:
                    best = cand
            ndp[i] = best
        dp = ndp
    return int(dp[n])


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["k"], obj["pages"]))


if __name__ == "__main__":
    main()

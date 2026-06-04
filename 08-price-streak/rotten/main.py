import json
import sys


def solve(seq):
    # Naive O(n^2) DP: correct, but TIMEOUTs on the large cases — the trap.
    n = len(seq)
    if n == 0:
        return 0
    dp = [1] * n
    for i in range(n):
        for j in range(i):
            if seq[j] < seq[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
    return max(dp)


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["seq"]))


if __name__ == "__main__":
    main()

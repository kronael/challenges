import json
import sys


def solve(seq):
    # Naive: for every price, rescan every earlier price as a predecessor.
    # Correct, but O(n^2) work TIMEOUTs on the large increasing sequence.
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

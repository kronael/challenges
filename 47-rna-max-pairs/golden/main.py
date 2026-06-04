import json
import sys


def can_pair(a, b, allow_wobble):
    pairs = {"AU", "UA", "CG", "GC"}
    if allow_wobble:
        pairs |= {"GU", "UG"}
    return a + b in pairs


def solve(rna, min_loop, allow_wobble):
    n = len(rna)
    # dp[i][j] = max pairs in rna[i..j] inclusive.
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for i in range(0, n - length + 1):
            j = i + length - 1
            best = dp[i][j - 1]  # j unpaired
            for k in range(i, j):
                if j - k > min_loop and can_pair(rna[k], rna[j], allow_wobble):
                    left = dp[i][k - 1] if k > i else 0
                    cand = left + 1 + dp[k + 1][j - 1]
                    if cand > best:
                        best = cand
            dp[i][j] = best
    return dp[0][n - 1] if n > 0 else 0


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["rna"], obj["min_loop"], obj["allow_wobble"]))


if __name__ == "__main__":
    main()

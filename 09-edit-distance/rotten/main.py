import json
import sys

sys.setrecursionlimit(1 << 20)


def solve(s, t):
    # Naive recursion: try every insert/delete/substitute, no memoization.
    # Correct, but exponential — it TIMEOUTs on the large cases (the trap).
    def rec(i, j):
        if i == 0:
            return j
        if j == 0:
            return i
        cost = 0 if s[i - 1] == t[j - 1] else 1
        return min(rec(i - 1, j) + 1, rec(i, j - 1) + 1, rec(i - 1, j - 1) + cost)

    return rec(len(s), len(t))


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["s"], obj["t"]))


if __name__ == "__main__":
    main()

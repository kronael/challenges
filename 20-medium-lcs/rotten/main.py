import json
import sys


def solve(s, t):
    # Naive exponential recursion: correct, but recomputes overlapping
    # subproblems — TIMEOUTs on the large cases. The trap.
    sys.setrecursionlimit(100000)

    def lcs(i, j):
        if i == 0 or j == 0:
            return 0
        if s[i - 1] == t[j - 1]:
            return lcs(i - 1, j - 1) + 1
        a = lcs(i - 1, j)
        b = lcs(i, j - 1)
        return a if a >= b else b

    return lcs(len(s), len(t))


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["s"], obj["t"]))


if __name__ == "__main__":
    main()

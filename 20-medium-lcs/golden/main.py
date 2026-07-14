import json
import sys


def solve(s, t):
    if len(t) > len(s):
        s, t = t, s
    m = len(t)
    prev = [0] * (m + 1)
    for c in s:
        cur = [0] * (m + 1)
        for j in range(1, m + 1):
            if c == t[j - 1]:
                cur[j] = prev[j - 1] + 1
            else:
                cur[j] = prev[j] if prev[j] >= cur[j - 1] else cur[j - 1]
        prev = cur
    return prev[m]


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["s"], obj["t"]))


if __name__ == "__main__":
    main()

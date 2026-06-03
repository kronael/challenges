import json
import sys


def solve(s, t):
    m = len(t)
    prev = list(range(m + 1))
    for i, cs in enumerate(s, 1):
        cur = [i] + [0] * m
        for j, ct in enumerate(t, 1):
            cost = 0 if cs == ct else 1
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost)
        prev = cur
    return prev[m]


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["s"], obj["t"]))


if __name__ == "__main__":
    main()

import json
import sys


def solve(text, pattern):
    m = len(pattern)
    if m == 0:
        return []
    fail = [0] * m
    k = 0
    for i in range(1, m):
        while k > 0 and pattern[i] != pattern[k]:
            k = fail[k - 1]
        if pattern[i] == pattern[k]:
            k += 1
        fail[i] = k
    res = []
    k = 0
    for i, c in enumerate(text):
        while k > 0 and c != pattern[k]:
            k = fail[k - 1]
        if c == pattern[k]:
            k += 1
        if k == m:
            res.append(i - m + 2)
            k = fail[k - 1]
    return res


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["text"], obj["pattern"]))


if __name__ == "__main__":
    main()

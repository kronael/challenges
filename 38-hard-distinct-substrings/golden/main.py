import json
import sys


def suffix_array(s):
    n = len(s)
    rank = [ord(c) for c in s]
    sa = list(range(n))
    tmp = [0] * n
    k = 1
    while True:
        second = rank + [-1] * k
        keys = [(rank[i], second[i + k]) for i in range(n)]
        sa.sort(key=keys.__getitem__)
        tmp[sa[0]] = 0
        for i in range(1, n):
            a, b = sa[i - 1], sa[i]
            tmp[b] = tmp[a] + (1 if keys[b] != keys[a] else 0)
        for i in range(n):
            rank[i] = tmp[i]
        if rank[sa[-1]] == n - 1:
            break
        k *= 2
    return sa, rank


def solve(s):
    n = len(s)
    if n == 0:
        return 0
    sa, rank = suffix_array(s)
    total = 0
    h = 0
    for i in range(n):
        if rank[i] > 0:
            j = sa[rank[i] - 1]
            while i + h < n and j + h < n and s[i + h] == s[j + h]:
                h += 1
            total += h
            if h > 0:
                h -= 1
        else:
            h = 0
    return n * (n + 1) // 2 - total


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["s"]))


if __name__ == "__main__":
    main()

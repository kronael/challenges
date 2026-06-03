import json
import sys


def solve(n, initial, queries):
    tree = [0] * (n + 1)

    def update(i, delta):
        while i <= n:
            tree[i] += delta
            i += i & (-i)

    def prefix_sum(i):
        s = 0
        while i > 0:
            s += tree[i]
            i -= i & (-i)
        return s

    for i, v in enumerate(initial, start=1):
        update(i, v)

    out = []
    for q in queries:
        if q[0] == "sum":
            out.append(prefix_sum(q[1]))
        else:
            update(q[1], q[2])
    return out


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["n"], obj["initial"], obj["queries"]))


if __name__ == "__main__":
    main()

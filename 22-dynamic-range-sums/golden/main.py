import json
import sys


def solve(n, values, ops):
    size = 1
    while size < n:
        size *= 2
    tree = [0] * (2 * size)
    for i in range(n):
        tree[size + i] = values[i]
    for i in range(size - 1, 0, -1):
        tree[i] = tree[2 * i] + tree[2 * i + 1]

    def update(i, v):
        i += size
        tree[i] = v
        i //= 2
        while i >= 1:
            tree[i] = tree[2 * i] + tree[2 * i + 1]
            i //= 2

    def query(lo, hi):
        lo += size
        hi += size + 1
        s = 0
        while lo < hi:
            if lo & 1:
                s += tree[lo]
                lo += 1
            if hi & 1:
                hi -= 1
                s += tree[hi]
            lo //= 2
            hi //= 2
        return s

    out = []
    for op in ops:
        if op[0] == "sum":
            out.append(query(op[1] - 1, op[2] - 1))
        else:
            update(op[1] - 1, op[2])
    return out


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["n"], obj["values"], obj["ops"]))


if __name__ == "__main__":
    main()

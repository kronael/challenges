import json
import sys


def solve(n, unions, queries):
    parent = list(range(n))
    rank = [0] * n

    def find(x):
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb:
            return
        if rank[ra] < rank[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        if rank[ra] == rank[rb]:
            rank[ra] += 1

    for a, b in unions:
        union(a, b)
    return [1 if find(u) == find(v) else 0 for u, v in queries]


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["n"], obj["unions"], obj["queries"]))


if __name__ == "__main__":
    main()

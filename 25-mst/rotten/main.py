import json
import sys


def solve(n, edges):
    # Naive Kruskal: correct, but TIMEOUTs on the large cases — the trap.
    # Instead of union-find, each candidate edge triggers a fresh BFS over the
    # partial tree to test connectivity. O(m * (n + m)).
    adj = [[] for _ in range(n)]
    total = 0
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        if not connected(adj, u, v):
            adj[u].append(v)
            adj[v].append(u)
            total += w
    return total


def connected(adj, src, dst):
    seen = [False] * len(adj)
    stack = [src]
    seen[src] = True
    while stack:
        x = stack.pop()
        if x == dst:
            return True
        for y in adj[x]:
            if not seen[y]:
                seen[y] = True
                stack.append(y)
    return False


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["n"], obj["edges"]))


if __name__ == "__main__":
    main()

import json
import sys


def solve(n, edges):
    # Naive O(n^2): scan all nodes each round to pick the closest unsettled one.
    # Correct, but TIMEOUTs on the large cases — the trap.
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    dist = [-1] * n
    dist[0] = 0
    done = [False] * n
    for _ in range(n):
        u = -1
        best = -1
        for i in range(n):
            if not done[i] and dist[i] != -1 and (best == -1 or dist[i] < best):
                best = dist[i]
                u = i
        if u == -1:
            break
        done[u] = True
        for v, w in adj[u]:
            nd = dist[u] + w
            if dist[v] == -1 or nd < dist[v]:
                dist[v] = nd
    return dist


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["n"], obj["edges"]))


if __name__ == "__main__":
    main()

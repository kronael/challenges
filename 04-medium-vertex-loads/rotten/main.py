import json
import sys
from collections import deque


def solve(n, edges, loads):
    # Naive: for every node, BFS outward to measure its distance to each fixed
    # node, then take the tightest lower bound (load - distance), floored at 0.
    # Correct, but a fresh O(V + E) BFS per node makes it O(V * (V + E)) — the
    # quadratic trap. TIMEOUTs on the large cases.
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    out = [0] * n
    for i, load in enumerate(loads):
        if load is not None:
            out[i] = load
            continue
        dist = [-1] * n
        dist[i] = 0
        q = deque([i])
        best = 0
        while q:
            u = q.popleft()
            src_load = loads[u]
            if src_load is not None:
                bound = src_load - dist[u]
                if bound > best:
                    best = bound
                continue  # bounds do not propagate past a fixed node
            for nb in adj[u]:
                if dist[nb] == -1:
                    dist[nb] = dist[u] + 1
                    q.append(nb)
        out[i] = best

    return out


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["n"], [tuple(e) for e in obj["edges"]], obj["loads"]))


if __name__ == "__main__":
    main()

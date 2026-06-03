import heapq
import json
import sys


def solve(n, edges, loads):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    dist = [-1] * n
    heap = []
    for i, load in enumerate(loads):
        if load is not None:
            dist[i] = load
            heapq.heappush(heap, (-load, i))

    while heap:
        neg_v, u = heapq.heappop(heap)
        v = -neg_v
        if dist[u] > v:
            continue
        new_v = v - 1
        for nb in adj[u]:
            if loads[nb] is not None:
                continue
            if new_v > dist[nb]:
                dist[nb] = new_v
                heapq.heappush(heap, (-new_v, nb))

    return [load if load is not None else max(0, dist[i]) for i, load in enumerate(loads)]


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["n"], [tuple(e) for e in obj["edges"]], obj["loads"]))


if __name__ == "__main__":
    main()

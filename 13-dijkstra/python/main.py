import heapq
import json
import sys


def solve(n, edges):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    dist = [-1] * n
    dist[0] = 0
    pq = [(0, 0)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            nd = d + w
            if dist[v] == -1 or nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["n"], obj["edges"]))


if __name__ == "__main__":
    main()

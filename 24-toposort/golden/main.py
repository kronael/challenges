import heapq
import json
import sys


def solve(n, edges):
    adj = [[] for _ in range(n)]
    indeg = [0] * n
    for u, v in edges:
        adj[u].append(v)
        indeg[v] += 1
    heap = [i for i in range(n) if indeg[i] == 0]
    heapq.heapify(heap)
    order = []
    while heap:
        u = heapq.heappop(heap)
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                heapq.heappush(heap, v)
    if len(order) != n:
        return "CYCLE"
    return order


def main():
    obj = json.load(sys.stdin)
    res = solve(obj["n"], obj["edges"])
    if res == "CYCLE":
        print("CYCLE")
    else:
        print(*res)


if __name__ == "__main__":
    main()

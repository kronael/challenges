import json
import sys
from collections import deque


def solve(n, edges):
    graph = [[] for _ in range(n + 1)]
    cap = []
    to = []

    def add_edge(u, v, c):
        graph[u].append(len(to))
        to.append(v)
        cap.append(c)
        graph[v].append(len(to))
        to.append(u)
        cap.append(0)

    for u, v, c in edges:
        add_edge(u, v, c)

    src, sink = 1, n

    def bfs(level):
        for i in range(n + 1):
            level[i] = -1
        level[src] = 0
        q = deque([src])
        while q:
            u = q.popleft()
            for eid in graph[u]:
                v = to[eid]
                if cap[eid] > 0 and level[v] == -1:
                    level[v] = level[u] + 1
                    q.append(v)
        return level[sink] != -1

    def dfs(u, pushed, level, it):
        if u == sink:
            return pushed
        while it[u] < len(graph[u]):
            eid = graph[u][it[u]]
            v = to[eid]
            if cap[eid] > 0 and level[v] == level[u] + 1:
                d = dfs(v, min(pushed, cap[eid]), level, it)
                if d > 0:
                    cap[eid] -= d
                    cap[eid ^ 1] += d
                    return d
            it[u] += 1
        return 0

    flow = 0
    level = [-1] * (n + 1)
    while bfs(level):
        it = [0] * (n + 1)
        while True:
            f = dfs(src, float("inf"), level, it)
            if f == 0:
                break
            flow += f
    return flow


def main():
    sys.setrecursionlimit(1 << 20)
    obj = json.load(sys.stdin)
    print(solve(obj["n"], obj["edges"]))


if __name__ == "__main__":
    main()

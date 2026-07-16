import json
import sys


def solve(n, edges):
    # Naive Ford-Fulkerson with DFS-found augmenting paths: correct, but each
    # augmentation may add one unit after scanning O(E) edges. The O(E * F)
    # worst case TIMEOUTs on the large cases, whose maximum flow F is large.
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

    def dfs(u, pushed, seen):
        if u == sink:
            return pushed
        seen[u] = True
        for eid in graph[u]:
            v = to[eid]
            if cap[eid] > 0 and not seen[v]:
                d = dfs(v, min(pushed, cap[eid]), seen)
                if d > 0:
                    cap[eid] -= d
                    cap[eid ^ 1] += d
                    return d
        return 0

    flow = 0
    while True:
        seen = [False] * (n + 1)
        f = dfs(src, float("inf"), seen)
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

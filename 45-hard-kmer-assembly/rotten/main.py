import json
import sys
from collections import defaultdict


def solve(k, kmers):
    if not kmers:
        return ""
    p = k - 1
    edges = [(km[:p], km[1:]) for km in kmers]
    used = [False] * len(edges)

    outdeg, indeg = defaultdict(int), defaultdict(int)
    for u, v in edges:
        outdeg[u] += 1
        indeg[v] += 1
    start = edges[0][0]
    for u in outdeg:
        if outdeg[u] - indeg[u] == 1:
            start = u
            break

    # Correct Hierholzer over the de Bruijn edges, but to leave a node it LINEAR-
    # SCANS the whole edge list for an unused out-edge: O(E) per edge, O(E^2) total
    # and independent of graph shape. Correct on the small cases, TIMEOUTs on the
    # large ones — the trap.
    stack = [start]
    path = []
    while stack:
        u = stack[-1]
        nxt = -1
        for i in range(len(edges)):
            if not used[i] and edges[i][0] == u:
                nxt = i
                break
        if nxt == -1:
            path.append(u)
            stack.pop()
        else:
            used[nxt] = True
            stack.append(edges[nxt][1])
    path.reverse()

    out = [path[0]]
    for node in path[1:]:
        out.append(node[-1])
    return "".join(out)


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["k"], obj["kmers"]))


if __name__ == "__main__":
    main()

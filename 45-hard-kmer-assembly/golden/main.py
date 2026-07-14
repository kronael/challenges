import json
import sys


def solve(k, kmers):
    if not kmers:
        return ""
    p = k - 1
    ids = {}
    adj = []

    def node(s):
        i = ids.get(s)
        if i is None:
            i = len(adj)
            ids[s] = i
            adj.append([])
        return i

    bal = []
    for km in kmers:
        u = node(km[:p])
        v = node(km[1:])
        adj[u].append(v)
        while len(bal) < len(adj):
            bal.append(0)
        bal[u] += 1
        bal[v] -= 1

    start = 0
    for i, b in enumerate(bal):
        if b == 1:
            start = i
            break

    labels = [None] * len(adj)
    for s, i in ids.items():
        labels[i] = s

    ptr = [0] * len(adj)
    stack = [start]
    path = []
    while stack:
        u = stack[-1]
        if ptr[u] < len(adj[u]):
            v = adj[u][ptr[u]]
            ptr[u] += 1
            stack.append(v)
        else:
            path.append(u)
            stack.pop()
    path.reverse()

    out = [labels[path[0]]]
    for v in path[1:]:
        out.append(labels[v][-1])
    return "".join(out)


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["k"], obj["kmers"]))


if __name__ == "__main__":
    main()

import json
import sys


def solve(n, parent, queries):
    # Naive: nothing is precomputed. Every pair rebuilds the first venue's whole
    # route to the root as a fresh list, then climbs from the second venue and
    # searches that list again at every step. Each search is a linear scan, and
    # every step before the shared venue scans the whole route without finding
    # anything, so a pair whose shared venue sits near the root costs
    # O(depth^2) — correct on the small cases, TIMEOUT on the large ones.
    del n
    out = []
    for a, b in queries:
        route = []
        node = a
        while node != -1:
            route.append(node)
            node = parent[node]
        node = b
        while node not in route:
            node = parent[node]
        out.append(node)
    return out


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["n"], obj["parent"], obj["queries"]))


if __name__ == "__main__":
    main()

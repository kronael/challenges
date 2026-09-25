import json
import sys


def solve(n, links):
    # Naive: nothing is shared between links. For every link in turn, rebuild the
    # whole adjacency without it and re-count the connected venue groups from
    # scratch; the link is critical exactly when the count goes up. Each count is
    # a full O(n + m) traversal of the network, so scanning all m links costs
    # O(m * (n + m)) — correct on the small cases, TIMEOUT on the large ones.
    whole = groups(n, links)
    return [
        link
        for link in range(len(links))
        if groups(n, links[:link] + links[link + 1 :]) > whole
    ]


def groups(n, links):
    adjacent = [[] for _ in range(n)]
    for u, v in links:
        adjacent[u].append(v)
        adjacent[v].append(u)
    seen = [False] * n
    count = 0
    for source in range(n):
        if seen[source]:
            continue
        count += 1
        seen[source] = True
        stack = [source]
        while stack:
            venue = stack.pop()
            for other in adjacent[venue]:
                if not seen[other]:
                    seen[other] = True
                    stack.append(other)
    return count


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["n"], obj["links"]))


if __name__ == "__main__":
    main()

import json
import sys


def solve(n, parent, queries):
    # Depth of every venue, once. Climb to the first venue whose depth is
    # already settled, then write the collected chain back down from there.
    # Every venue is settled exactly once, so the whole pass is O(n), and it
    # walks the parent links instead of recursing — the hierarchy can be a
    # 200000-deep line.
    depth = [-1] * n
    for start in range(n):
        chain = []
        node = start
        while node != -1 and depth[node] < 0:
            chain.append(node)
            node = parent[node]
        level = 0 if node == -1 else depth[node] + 1
        for venue in reversed(chain):
            depth[venue] = level
            level += 1

    # Per pair: lift the deeper venue to the shallower one's level, then step
    # both up in lockstep. Equal depths meet for the first time exactly at the
    # deepest shared venue, so the pair costs O(distance to that venue).
    out = []
    for a, b in queries:
        if depth[a] < depth[b]:
            a, b = b, a
        while depth[a] > depth[b]:
            a = parent[a]
        while a != b:
            a = parent[a]
            b = parent[b]
        out.append(a)
    return out


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["n"], obj["parent"], obj["queries"]))


if __name__ == "__main__":
    main()

import json
import sys


def solve(n, edges):
    # Naive: at each step, linearly scan ALL n nodes to find the smallest one
    # whose prerequisites are all done. Correct (same order as the heap), but
    # O(n^2) — it TIMEOUTs on the large cases. The trap.
    adj = [[] for _ in range(n)]
    indeg = [0] * n
    for u, v in edges:
        adj[u].append(v)
        indeg[v] += 1
    done = [False] * n
    order = []
    for _ in range(n):
        pick = -1
        for i in range(n):
            if not done[i] and indeg[i] == 0:
                pick = i
                break
        if pick == -1:
            return "CYCLE"
        done[pick] = True
        order.append(pick)
        for v in adj[pick]:
            indeg[v] -= 1
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

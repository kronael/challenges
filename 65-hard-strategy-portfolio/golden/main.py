import json
import sys
from collections import deque


def solve(n, pnl, requires):
    # Every valid activation set is a subset closed under `requires`, and the
    # complement of a closed subset is what a cut separates: read the strategies
    # as nodes of a flow network with a source feeding every earner its own
    # profit, every loss-maker draining its own loss into the sink, and each
    # prerequisite as an arc of capacity `infinite` from the strategy to what it
    # needs. No finite cut can sever a prerequisite arc, so the source side of
    # any finite cut is exactly a valid activation set, its capacity is the
    # profit given up plus the losses taken on, and the best set costs the
    # least. So the answer is the total of the positive contributions minus the
    # smallest cut, which by max-flow/min-cut is the largest flow.
    source = n
    sink = n + 1
    size = n + 2
    graph = [[] for _ in range(size)]
    to = []
    cap = []

    def add_edge(u, v, capacity):
        graph[u].append(len(to))
        to.append(v)
        cap.append(capacity)
        graph[v].append(len(to))
        to.append(u)
        cap.append(0)

    total_positive = 0
    for strategy, value in enumerate(pnl):
        if value > 0:
            total_positive += value
            add_edge(source, strategy, value)
        elif value < 0:
            add_edge(strategy, sink, -value)

    # One more than any cut that cuts only source and sink arcs, so a cut that
    # severs a prerequisite arc is never the cheapest one. A strategy listing
    # itself needs no special case: the arc leaves and enters the same node, so
    # neither search below can ever traverse it.
    infinite = total_positive + 1
    for a, b in requires:
        add_edge(a, b, infinite)

    level = [-1] * size
    progress = [0] * size

    def relabel():
        for node in range(size):
            level[node] = -1
        level[source] = 0
        queue = deque([source])
        while queue:
            node = queue.popleft()
            for eid in graph[node]:
                target = to[eid]
                if cap[eid] > 0 and level[target] < 0:
                    level[target] = level[node] + 1
                    queue.append(target)
        return level[sink] >= 0

    # Dinic: each phase relabels every node with its distance from the source in
    # the residual network, then saturates every shortest source-to-sink route
    # before relabelling again. The route search is an explicit stack, since a
    # prerequisite list is allowed to be one long chain and the routes are then
    # as deep as the chain.
    flow = 0
    while relabel():
        for node in range(size):
            progress[node] = 0
        path = []
        node = source
        while True:
            if node == sink:
                pushed = min(cap[eid] for eid in path)
                for eid in path:
                    cap[eid] -= pushed
                    cap[eid ^ 1] += pushed
                flow += pushed
                cut = next(depth for depth, eid in enumerate(path) if cap[eid] == 0)
                node = to[path[cut] ^ 1]
                del path[cut:]
                continue
            advanced = False
            while progress[node] < len(graph[node]):
                eid = graph[node][progress[node]]
                target = to[eid]
                if cap[eid] > 0 and level[target] == level[node] + 1:
                    path.append(eid)
                    node = target
                    advanced = True
                    break
                progress[node] += 1
            if advanced:
                continue
            level[node] = -1
            if not path:
                break
            eid = path.pop()
            node = to[eid ^ 1]
            progress[node] += 1
    return total_positive - flow


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["n"], obj["pnl"], obj["requires"]))


if __name__ == "__main__":
    main()

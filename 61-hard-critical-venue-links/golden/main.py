import json
import sys


def solve(n, links):
    m = len(links)

    # Flat adjacency in one pass over the links: counting sort the endpoints into
    # `slot_to` / `slot_link`, so venue v owns slots start[v] .. start[v+1]-1 and
    # every slot remembers which link it came from. The link number is what makes
    # the walk below able to tell two links between the same pair of venues apart.
    degree = [0] * (n + 1)
    for u, v in links:
        degree[u] += 1
        degree[v] += 1
    start = [0] * (n + 1)
    running = 0
    for venue in range(n):
        start[venue] = running
        running += degree[venue]
    start[n] = running
    fill = start[:]
    slot_to = [0] * (2 * m)
    slot_link = [0] * (2 * m)
    for link, (u, v) in enumerate(links):
        slot = fill[u]
        fill[u] = slot + 1
        slot_to[slot] = v
        slot_link[slot] = link
        slot = fill[v]
        fill[v] = slot + 1
        slot_to[slot] = u
        slot_link[slot] = link

    # One depth-first walk over the whole network. `order[v]` is the step at which
    # v was first reached; `reach[v]` is the smallest order reachable from v's
    # subtree using subtree links plus at most one link back up. A tree link into
    # v is critical exactly when reach[v] > order[parent]: nothing under v gets
    # back to or above the parent without it.
    #
    # The walk is an explicit stack, not recursion: the network can be a single
    # 200000-venue line, so a recursive walk would be 200000 frames deep.
    order = [-1] * n
    reach = [0] * n
    entered = [-1] * n  # link number the walk used to enter each venue
    cursor = start[:]  # next unexamined slot per venue
    step = 0
    critical = []
    stack = []
    for root in range(n):
        if order[root] >= 0:
            continue
        order[root] = reach[root] = step
        step += 1
        stack.append(root)
        while stack:
            venue = stack[-1]
            slot = cursor[venue]
            if slot < start[venue + 1]:
                cursor[venue] = slot + 1
                link = slot_link[slot]
                # Skip only the one slot holding the link we arrived on. A second
                # link between the same two venues has a different number, so it
                # still counts as a way back up — and that is why a doubled link
                # is never critical.
                if link == entered[venue]:
                    continue
                other = slot_to[slot]
                if order[other] < 0:
                    entered[other] = link
                    order[other] = reach[other] = step
                    step += 1
                    stack.append(other)
                elif order[other] < reach[venue]:
                    reach[venue] = order[other]
            else:
                stack.pop()
                if stack:
                    parent = stack[-1]
                    if reach[venue] < reach[parent]:
                        reach[parent] = reach[venue]
                    if reach[venue] > order[parent]:
                        critical.append(entered[venue])

    critical.sort()
    return critical


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["n"], obj["links"]))


if __name__ == "__main__":
    main()

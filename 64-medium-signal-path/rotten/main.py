import json
import sys


def solve(n, root, pnl, left, right):
    del root

    # Naive: take every desk in turn as the desk where the chain meets, and for
    # each of its children walk that child's whole subtree from scratch, carrying
    # the running total downward, to find the best descending chain there. A desk
    # shares nothing with its parent, so the walk over a subtree is repeated once
    # for every desk above it: the total work is the sum of all subtree sizes,
    # which is O(n^2) on a deep hierarchy. Fine on the small cases; on a
    # 500000-desk chain it is about n^2/2 = 1.25 * 10^11 steps, so both large
    # cases TIMEOUT.
    def best_descending(start):
        best = pnl[start]
        stack = [(start, best)]
        while stack:
            node, total = stack.pop()
            if total > best:
                best = total
            for child in (left[node], right[node]):
                if child >= 0:
                    stack.append((child, total + pnl[child]))
        return best

    answer = None
    for node in range(n):
        meeting = pnl[node]
        for child in (left[node], right[node]):
            if child >= 0:
                gain = best_descending(child)
                if gain > 0:
                    meeting += gain
        if answer is None or meeting > answer:
            answer = meeting
    return answer


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["n"], obj["root"], obj["pnl"], obj["left"], obj["right"]))


if __name__ == "__main__":
    main()

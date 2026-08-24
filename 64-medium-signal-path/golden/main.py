import json
import sys


def solve(n, root, pnl, left, right):
    # One bottom-up pass. `down[node]` is the best total of a chain that starts
    # at `node` and only ever descends; a child whose own best descending chain
    # is negative is worth 0 rather than worth taking, which is what the two
    # `> 0` tests below decide. Each desk then answers two different questions:
    # the chain that meets at it may use both children, while the value handed
    # to its parent may use only the better one, since a chain cannot leave the
    # parent twice.
    #
    # The traversal is an explicit stack, not recursion: the hierarchy can be a
    # single 500000-desk line, so a recursive walk would be 500000 frames deep.
    # A stack-built preorder, read back to front, settles every child before its
    # parent, because a preorder lists a desk ahead of all of its descendants.
    order = []
    stack = [root]
    while stack:
        node = stack.pop()
        order.append(node)
        first = left[node]
        if first >= 0:
            stack.append(first)
        second = right[node]
        if second >= 0:
            stack.append(second)

    down = [0] * n
    best = None
    for node in reversed(order):
        first = left[node]
        gain_first = down[first] if first >= 0 and down[first] > 0 else 0
        second = right[node]
        gain_second = down[second] if second >= 0 and down[second] > 0 else 0
        meeting = pnl[node] + gain_first + gain_second
        if best is None or meeting > best:
            best = meeting
        down[node] = pnl[node] + (
            gain_first if gain_first > gain_second else gain_second
        )
    return best


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["n"], obj["root"], obj["pnl"], obj["left"], obj["right"]))


if __name__ == "__main__":
    main()

import json
import sys

sys.setrecursionlimit(1 << 20)


class Rope:
    __slots__ = ("s", "left", "right", "weight", "length")

    def __init__(self, s=None, left=None, right=None):
        if s is not None:
            self.s = s
            self.left = None
            self.right = None
            self.weight = len(s)
            self.length = len(s)
        else:
            self.s = None
            self.left = left
            self.right = right
            self.weight = left.length
            self.length = left.length + right.length


def build(parts):
    # Naive left fold: builds a degenerate right-leaning chain of depth O(n).
    root = None
    for p in parts:
        if p == "":
            continue
        node = Rope(p)
        root = node if root is None else Rope(left=root, right=node)
    return root


def index(node, i):
    # Recursive descent from the root for a single character — O(depth) per lookup.
    if node.s is not None:
        return node.s[i]
    if i < node.weight:
        return index(node.left, i)
    return index(node.right, i - node.weight)


def solve(parts, queries):
    # Naive: index the rope one character at a time, re-descending the whole
    # chain for every position. Correct, but TIMEOUTs on the large cases.
    root = build(parts)
    total = root.length if root is not None else 0
    res = []
    for lo, hi in queries:
        lo = max(0, lo)
        hi = min(total, hi)
        res.append("".join(index(root, i) for i in range(lo, hi)) if lo < hi else "")
    return "|".join(res)


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["parts"], obj["queries"]))


if __name__ == "__main__":
    main()

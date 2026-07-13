import json
import sys


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


def concat(a, b):
    if a is None:
        return b
    if b is None:
        return a
    return Rope(left=a, right=b)


def build(parts):
    # Balanced merge: O(n log n) tree depth, avoids the degenerate
    # right-leaning chain a naive left fold would produce.
    nodes = [Rope(p) for p in parts if p != ""]
    if not nodes:
        return None
    while len(nodes) > 1:
        merged = []
        for i in range(0, len(nodes), 2):
            if i + 1 < len(nodes):
                merged.append(concat(nodes[i], nodes[i + 1]))
            else:
                merged.append(nodes[i])
        nodes = merged
    return nodes[0]


def extract(node, lo, hi):
    # Collect characters of [lo, hi) into out, walking the tree by weight.
    out = []
    _extract(node, lo, hi, out)
    return "".join(out)


def _extract(node, lo, hi, out):
    if node is None or lo >= hi:
        return
    if node.s is not None:
        out.append(node.s[lo:hi])
        return
    w = node.weight
    if lo < w:
        _extract(node.left, lo, min(hi, w), out)
    if hi > w:
        _extract(node.right, max(lo - w, 0), hi - w, out)


def solve(parts, queries):
    root = build(parts)
    total = root.length if root is not None else 0
    res = []
    for lo, hi in queries:
        lo = max(0, lo)
        hi = min(total, hi)
        res.append(extract(root, lo, hi) if lo < hi else "")
    return "|".join(res)


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["parts"], obj["queries"]))


if __name__ == "__main__":
    main()

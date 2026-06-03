import json
import sys


class Node:
    __slots__ = ("kids", "end")

    def __init__(self):
        self.kids = {}
        self.end = False


def solve(words, queries):
    root = Node()
    for w in words:
        node = root
        for ch in w:
            node = node.kids.setdefault(ch, Node())
        node.end = True

    results = []
    for q in queries:
        node = root
        ok = True
        for ch in q:
            nxt = node.kids.get(ch)
            if nxt is None:
                ok = False
                break
            node = nxt
        if not ok:
            results.append("")
            continue
        found = []
        stack = [(node, q)]
        # iterative pre-order DFS, children visited in a-z order
        while stack and len(found) < 3:
            cur, prefix = stack.pop()
            if cur.end:
                found.append(prefix)
                if len(found) == 3:
                    break
            for ch in sorted(cur.kids, reverse=True):
                stack.append((cur.kids[ch], prefix + ch))
        results.append(" ".join(found))
    return ";".join(results)


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["words"], obj["queries"]))


if __name__ == "__main__":
    main()

import json
import sys


class RollbackDSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.history = []

    def find(self, node):
        while self.parent[node] != node:
            node = self.parent[node]
        return node

    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)
        if a == b:
            return
        if self.size[a] < self.size[b]:
            a, b = b, a
        self.history.append((b, self.size[a]))
        self.parent[b] = a
        self.size[a] += self.size[b]

    def snapshot(self):
        return len(self.history)

    def rollback(self, snapshot):
        while len(self.history) > snapshot:
            child, old_size = self.history.pop()
            root = self.parent[child]
            self.size[root] = old_size
            self.parent[child] = child


def solve(n, operations):
    count = len(operations)
    tree = [[] for _ in range(max(1, 4 * count))]
    opened = {}

    def edge(op):
        return tuple(sorted((op["u"], op["v"])))

    def add_interval(node, left, right, start, end, value):
        if start >= right or end <= left:
            return
        if start <= left and right <= end:
            tree[node].append(value)
            return
        middle = (left + right) // 2
        add_interval(node * 2, left, middle, start, end, value)
        add_interval(node * 2 + 1, middle, right, start, end, value)

    for time, op in enumerate(operations):
        value = edge(op)
        if op["type"] == "add":
            opened[value] = time
        elif op["type"] == "remove":
            add_interval(1, 0, count, opened.pop(value), time, value)
    for value, start in opened.items():
        add_interval(1, 0, count, start, count, value)

    answers = []
    dsu = RollbackDSU(n)

    def visit(node, left, right):
        snapshot = dsu.snapshot()
        for a, b in tree[node]:
            dsu.union(a, b)
        if right - left == 1:
            op = operations[left]
            if op["type"] == "ask":
                answers.append(int(dsu.find(op["u"]) == dsu.find(op["v"])))
        else:
            middle = (left + right) // 2
            visit(node * 2, left, middle)
            visit(node * 2 + 1, middle, right)
        dsu.rollback(snapshot)

    if count:
        visit(1, 0, count)
    return answers


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["n"], obj["operations"]))


if __name__ == "__main__":
    main()

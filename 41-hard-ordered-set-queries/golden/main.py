import json
import random
import sys

MAX_LEVEL = 20
P = 0.5


class Node:
    __slots__ = ("val", "next", "width")

    def __init__(self, val, level):
        self.val = val
        self.next = [None] * level
        # width[i] = number of level-0 nodes from this node (exclusive) up to and
        # including next[i]; 0 when next[i] is None. Turns range_count into a
        # difference of ranks, so a full-domain query is O(log n), not O(range).
        self.width = [0] * level


class SkipList:
    def __init__(self, seed=12345):
        self.rng = random.Random(seed)
        self.head = Node(None, MAX_LEVEL)
        self.level = 1
        self.size = 0

    def _random_level(self):
        lvl = 1
        while lvl < MAX_LEVEL and self.rng.random() < P:
            lvl += 1
        return lvl

    def search(self, val):
        cur = self.head
        for i in range(self.level - 1, -1, -1):
            while cur.next[i] is not None and cur.next[i].val < val:
                cur = cur.next[i]
        cur = cur.next[0]
        return cur is not None and cur.val == val

    def insert(self, val):
        update = [self.head] * MAX_LEVEL
        rank = [0] * MAX_LEVEL
        cur = self.head
        for i in range(self.level - 1, -1, -1):
            rank[i] = 0 if i == self.level - 1 else rank[i + 1]
            while cur.next[i] is not None and cur.next[i].val < val:
                rank[i] += cur.width[i]
                cur = cur.next[i]
            update[i] = cur
        nxt = cur.next[0]
        if nxt is not None and nxt.val == val:
            return
        lvl = self._random_level()
        if lvl > self.level:
            for i in range(self.level, lvl):
                rank[i] = 0
                update[i] = self.head
                self.head.width[i] = self.size
            self.level = lvl
        node = Node(val, lvl)
        for i in range(lvl):
            node.next[i] = update[i].next[i]
            update[i].next[i] = node
            node.width[i] = update[i].width[i] - (rank[0] - rank[i])
            update[i].width[i] = (rank[0] - rank[i]) + 1
        for i in range(lvl, self.level):
            update[i].width[i] += 1
        self.size += 1

    def delete(self, val):
        update = [self.head] * MAX_LEVEL
        cur = self.head
        for i in range(self.level - 1, -1, -1):
            while cur.next[i] is not None and cur.next[i].val < val:
                cur = cur.next[i]
            update[i] = cur
        cur = cur.next[0]
        if cur is None or cur.val != val:
            return
        for i in range(self.level):
            if update[i].next[i] is cur:
                update[i].width[i] += cur.width[i] - 1
                update[i].next[i] = cur.next[i]
            else:
                update[i].width[i] -= 1
        while self.level > 1 and self.head.next[self.level - 1] is None:
            self.level -= 1
        self.size -= 1

    def _count_lt(self, val):
        cur = self.head
        rank = 0
        for i in range(self.level - 1, -1, -1):
            while cur.next[i] is not None and cur.next[i].val < val:
                rank += cur.width[i]
                cur = cur.next[i]
        return rank

    def range_count(self, lo, hi):
        return self._count_lt(hi + 1) - self._count_lt(lo)


def solve(ops):
    sl = SkipList()
    out = []
    for op in ops:
        kind = op[0]
        if kind == "insert":
            sl.insert(op[1])
        elif kind == "delete":
            sl.delete(op[1])
        elif kind == "search":
            out.append(1 if sl.search(op[1]) else 0)
        elif kind == "range_count":
            out.append(sl.range_count(op[1], op[2]))
    return out


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["ops"]))


if __name__ == "__main__":
    main()

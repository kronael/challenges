import json
import random
import sys

MAX_LEVEL = 20
P = 0.5


class Node:
    __slots__ = ("val", "next")

    def __init__(self, val, level):
        self.val = val
        self.next = [None] * level


class SkipList:
    def __init__(self, seed=12345):
        self.rng = random.Random(seed)
        self.head = Node(None, MAX_LEVEL)
        self.level = 1

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
        cur = self.head
        for i in range(self.level - 1, -1, -1):
            while cur.next[i] is not None and cur.next[i].val < val:
                cur = cur.next[i]
            update[i] = cur
        cur = cur.next[0]
        if cur is not None and cur.val == val:
            return
        lvl = self._random_level()
        if lvl > self.level:
            for i in range(self.level, lvl):
                update[i] = self.head
            self.level = lvl
        node = Node(val, lvl)
        for i in range(lvl):
            node.next[i] = update[i].next[i]
            update[i].next[i] = node

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
            if update[i].next[i] is not cur:
                break
            update[i].next[i] = cur.next[i]
        while self.level > 1 and self.head.next[self.level - 1] is None:
            self.level -= 1

    def range_count(self, lo, hi):
        cur = self.head
        for i in range(self.level - 1, -1, -1):
            while cur.next[i] is not None and cur.next[i].val < lo:
                cur = cur.next[i]
        cur = cur.next[0]
        count = 0
        while cur is not None and cur.val <= hi:
            count += 1
            cur = cur.next[0]
        return count


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

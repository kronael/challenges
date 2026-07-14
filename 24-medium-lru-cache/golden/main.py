import json
import sys


class Node:
    __slots__ = ("key", "val", "prev", "next")

    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None


def solve(capacity, ops):
    table = {}
    head = Node()  # sentinel; head.next is MRU
    tail = Node()  # sentinel; tail.prev is LRU
    head.next = tail
    tail.prev = head

    def remove(node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def push_front(node):
        node.prev = head
        node.next = head.next
        head.next.prev = node
        head.next = node

    out = []
    for op in ops:
        if op[0] == "get":
            node = table.get(op[1])
            if node is None:
                out.append(-1)
            else:
                remove(node)
                push_front(node)
                out.append(node.val)
        else:  # put
            key, val = op[1], op[2]
            node = table.get(key)
            if node is not None:
                node.val = val
                remove(node)
                push_front(node)
            else:
                node = Node(key, val)
                table[key] = node
                push_front(node)
                if len(table) > capacity:
                    lru = tail.prev
                    remove(lru)
                    del table[lru.key]
    return out


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["capacity"], obj["ops"]))


if __name__ == "__main__":
    main()

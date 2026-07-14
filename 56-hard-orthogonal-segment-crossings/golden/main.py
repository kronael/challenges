import json
import sys
from bisect import bisect_left, bisect_right


class Fenwick:
    def __init__(self, size):
        self.tree = [0] * (size + 1)

    def add(self, index, delta):
        index += 1
        while index < len(self.tree):
            self.tree[index] += delta
            index += index & -index

    def prefix(self, end):
        total = 0
        while end > 0:
            total += self.tree[end]
            end -= end & -end
        return total


def solve(horizontal, vertical):
    ys = sorted({segment[2] for segment in horizontal})
    positions = {value: i for i, value in enumerate(ys)}
    events = []
    for x1, x2, y in horizontal:
        events.append((x1, 0, y, 0))
        events.append((x2, 2, y, 0))
    for x, y1, y2 in vertical:
        events.append((x, 1, y1, y2))
    events.sort()

    active = Fenwick(len(ys))
    crossings = 0
    for _, kind, a, b in events:
        if kind == 0:
            active.add(positions[a], 1)
        elif kind == 2:
            active.add(positions[a], -1)
        else:
            left = bisect_left(ys, a)
            right = bisect_right(ys, b)
            crossings += active.prefix(right) - active.prefix(left)
    return crossings


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["horizontal"], obj["vertical"]))


if __name__ == "__main__":
    main()

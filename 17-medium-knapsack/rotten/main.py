import json
import sys


def solve(capacity, items):
    # Naive exponential take/skip recursion: correct, but explores 2^n subsets —
    # it TIMEOUTs on the large cases (the trap).
    def best(i, room):
        if i == len(items):
            return 0
        skip = best(i + 1, room)
        w = items[i]["weight"]
        if w > room:
            return skip
        take = items[i]["value"] + best(i + 1, room - w)
        return take if take > skip else skip

    return best(0, capacity)


def main():
    sys.setrecursionlimit(1 << 20)
    obj = json.load(sys.stdin)
    print(solve(obj["capacity"], obj["items"]))


if __name__ == "__main__":
    main()

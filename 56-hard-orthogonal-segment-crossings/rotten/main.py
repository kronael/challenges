import json
import sys


def solve(horizontal, vertical):
    crossings = 0
    # Naive: test every horizontal-vertical pair directly. Correct, but O(H*V)
    # coordinate comparisons TIMEOUT on both large segment sets.
    for x1, x2, y in horizontal:
        for x, y1, y2 in vertical:
            if x1 <= x <= x2 and y1 <= y <= y2:
                crossings += 1
    return crossings


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["horizontal"], obj["vertical"]))


if __name__ == "__main__":
    main()

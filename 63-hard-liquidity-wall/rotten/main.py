import json
import sys


def solve(n, quantities):
    # Naive: for every level, walk outward in both directions to find how far a
    # sweep at that level's own resting quantity can reach, then size that block.
    # Each level rediscovers its whole run from scratch and shares nothing with
    # its neighbours, so this is O(n^2). Fine on the small cases; on a book whose
    # quantities only ever grow, every walk runs to the far end, which is about
    # n^2/2 = 5 * 10^11 comparisons at n = 1000000, so both large cases TIMEOUT.
    best = 0
    for i in range(n):
        quantity = quantities[i]
        left = i
        while left > 0 and quantities[left - 1] >= quantity:
            left -= 1
        right = i
        while right + 1 < n and quantities[right + 1] >= quantity:
            right += 1
        area = quantity * (right - left + 1)
        if area > best:
            best = area
    return best


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["n"], obj["quantities"]))


if __name__ == "__main__":
    main()

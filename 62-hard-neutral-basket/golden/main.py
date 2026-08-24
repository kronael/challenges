import json
import sys
from bisect import bisect_left


def basket_totals(values):
    # Every subset total of `values`, built by doubling: each new position either
    # joins a basket already listed or does not. 2^len(values) totals, and the
    # empty basket's 0 is the first of them.
    totals = [0]
    for value in values:
        totals += [total + value for total in totals]
    return totals


def solve(n, target, exposures):
    # Meet in the middle. Split the book in half, list the subset totals of each
    # half separately, and sort one side. Every basket is one total from the left
    # plus one from the right, so the best partner of a left total is whichever
    # right total sits closest to `target - total` — a binary search, not a scan.
    # That is 2 * 2^(n/2) totals and 2^(n/2) searches instead of 2^n baskets.
    middle = n // 2
    left = basket_totals(exposures[:middle])
    right = sorted(basket_totals(exposures[middle:]))
    limit = len(right)

    # The empty basket is a valid choice, and it is the pair (0, 0) below, so
    # |target| is both the starting bound and a total the loop would find anyway.
    best = abs(target)
    for total in left:
        want = target - total
        index = bisect_left(right, want)
        if index < limit:
            gap = right[index] - want
            if gap < best:
                best = gap
        if index > 0:
            gap = want - right[index - 1]
            if gap < best:
                best = gap
    return best


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["n"], obj["target"], obj["exposures"]))


if __name__ == "__main__":
    main()

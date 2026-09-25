import json
import random
import sys


def kth_largest(values, k):
    # Quickselect with a random pivot and a three-way (Dutch flag) partition.
    # Only the side holding rank k survives each round, so the expected work is
    # n + n/2 + n/4 + ... = O(n). The equal band makes a heavy duplicate cluster
    # one round of work instead of a re-partitioned tail.
    rng = random.Random(0x5EED)
    target = k - 1
    lo, hi = 0, len(values) - 1
    while lo < hi:
        pivot = values[rng.randint(lo, hi)]
        i = mid = lo
        gt = hi
        while mid <= gt:
            value = values[mid]
            if value > pivot:
                values[i], values[mid] = values[mid], values[i]
                i += 1
                mid += 1
            elif value < pivot:
                values[mid], values[gt] = values[gt], values[mid]
                gt -= 1
            else:
                mid += 1
        # values[lo:i] > pivot, values[i:gt+1] == pivot, values[gt+1:hi+1] < pivot
        if target < i:
            hi = i - 1
        elif target <= gt:
            return pivot
        else:
            lo = gt + 1
    return values[lo]


def solve(n, slippage, ks):
    del n
    return [kth_largest(list(slippage), k) for k in ks]


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["n"], obj["slippage"], obj["ks"]))


if __name__ == "__main__":
    main()

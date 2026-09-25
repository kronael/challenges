import json
import sys


def solve(n, pnl, requires):
    # Naive: enumerate every activation set there is, drop the ones that
    # activate a strategy without one of its prerequisites, and keep the best
    # total. Correct for any input the README allows, and the count of candidates
    # doubles with every strategy: 2^n subsets, each costing O(n + m) to check
    # and score. The large cases have n in the tens of thousands, so this never
    # finishes.
    best = 0
    for mask in range(1 << n):
        if all(not (mask >> a & 1) or mask >> b & 1 for a, b in requires):
            best = max(best, sum(pnl[i] for i in range(n) if mask >> i & 1))
    return best


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["n"], obj["pnl"], obj["requires"]))


if __name__ == "__main__":
    main()

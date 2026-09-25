import json
import sys


def solve(n, prices):
    # Monotonic stack of days whose undercut is still unknown; their prices are
    # non-decreasing from bottom to top, so today closes a run at the top and
    # stops at the first day it does not undercut. Each day is pushed once and
    # popped at most once: one linear pass over the series.
    out = [0] * n
    open_days = []
    for i, price in enumerate(prices):
        while open_days and prices[open_days[-1]] > price:
            day = open_days.pop()
            out[day] = i - day
        open_days.append(i)
    return out


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["n"], obj["prices"]))


if __name__ == "__main__":
    main()

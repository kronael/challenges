import json
import sys


def solve(n, values, ops):
    # Naive: plain array, rescan the range on every sum — O(n) per query.
    # Correct, but TIMEOUTs on the large cases — the trap.
    a = list(values)
    out = []
    for op in ops:
        if op[0] == "sum":
            lo, hi = op[1] - 1, op[2] - 1
            s = 0
            for i in range(lo, hi + 1):
                s += a[i]
            out.append(s)
        else:
            a[op[1] - 1] = op[2]
    return out


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["n"], obj["values"], obj["ops"]))


if __name__ == "__main__":
    main()

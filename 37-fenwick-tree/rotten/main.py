import json
import sys


def solve(n, initial, queries):
    # Naive: keep the raw array; every "sum i" rescans a[1..i] in O(n).
    # Correct, but O(n) per query TIMEOUTs on the large cases — the trap.
    a = [0] + list(initial)
    out = []
    for q in queries:
        if q[0] == "sum":
            i = q[1]
            out.append(sum(a[1 : i + 1]))
        else:
            a[q[1]] += q[2]
    return out


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["n"], obj["initial"], obj["queries"]))


if __name__ == "__main__":
    main()

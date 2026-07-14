import json
import sys


def solve(stream):
    # Naive: re-sort the whole prefix at every step and read its middle.
    # O(n log n) per insertion → O(n^2 log n) overall, so it TIMEOUTs on the
    # large cases — the trap.
    s = []
    out = []
    for x in stream:
        s.append(x)
        t = sorted(s)
        n = len(t)
        if n % 2:
            out.append(str(t[n // 2]))
        else:
            out.append(f"{(t[n // 2 - 1] + t[n // 2]) / 2:.1f}")
    return out


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["stream"]))


if __name__ == "__main__":
    main()

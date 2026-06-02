import heapq
import json
import sys


def solve(stream):
    lo = []  # max-heap (values negated): lower half
    hi = []  # min-heap: upper half
    out = []
    for x in stream:
        if lo and x > -lo[0]:
            heapq.heappush(hi, x)
        else:
            heapq.heappush(lo, -x)
        if len(lo) > len(hi) + 1:
            heapq.heappush(hi, -heapq.heappop(lo))
        elif len(hi) > len(lo):
            heapq.heappush(lo, -heapq.heappop(hi))
        if len(lo) > len(hi):
            out.append(str(-lo[0]))
        else:
            out.append(f"{(-lo[0] + hi[0]) / 2:.1f}")
    return out


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["stream"]))


if __name__ == "__main__":
    main()

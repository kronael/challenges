import json
import sys
from collections import deque


def solve(k, arr):
    dq = deque()  # indices, values decreasing
    out = []
    for i, x in enumerate(arr):
        while dq and arr[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            out.append(arr[dq[0]])
    return out


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["k"], obj["arr"]))


if __name__ == "__main__":
    main()

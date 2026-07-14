import json
import sys


def solve(arr):
    # Naive O(n^2): try every (start, end) pair — correct, but TIMEOUTs on the large
    # cases. The trap: at n=10^6 the quadratic scan never finishes.
    n = len(arr)
    best = arr[0]
    for i in range(n):
        s = 0
        for j in range(i, n):
            s += arr[j]
            if s > best:
                best = s
    return best


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["arr"]))


if __name__ == "__main__":
    main()

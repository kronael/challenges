import json
import sys


def solve(k, arr):
    # Naive O(n*k): rescan max(arr[i:i+k]) for every window — the trap.
    # Correct, but TIMEOUTs on the large cases.
    n = len(arr)
    out = []
    for i in range(n - k + 1):
        m = arr[i]
        for j in range(i + 1, i + k):
            if arr[j] > m:
                m = arr[j]
        out.append(m)
    return out


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["k"], obj["arr"]))


if __name__ == "__main__":
    main()

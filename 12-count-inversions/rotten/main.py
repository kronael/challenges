import json
import sys


def solve(arr):
    # Naive O(n^2) double loop: correct, but TIMEOUTs on the large cases — the trap.
    n = len(arr)
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                count += 1
    return count


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["arr"]))


if __name__ == "__main__":
    main()

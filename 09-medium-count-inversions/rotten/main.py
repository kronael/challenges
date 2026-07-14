import json
import sys


def solve(arr):
    # Naive: inspect every index pair and count the out-of-order ones directly.
    # Correct, but O(n^2) work TIMEOUTs on the large reversed array.
    n = len(arr)
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                count += 1
    return count


def main():
    obj = json.load(sys.stdin)
    arr = obj["arr"]
    if obj["n"] != len(arr):
        raise ValueError("n must match len(arr)")
    print(solve(arr))


if __name__ == "__main__":
    main()

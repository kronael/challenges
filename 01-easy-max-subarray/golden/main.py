import json
import sys


def solve(arr):
    best = cur = arr[0]
    for x in arr[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["arr"]))


if __name__ == "__main__":
    main()

import json
import sys


def solve(arr):
    # TODO: return the number of inversions (pairs i < j with arr[i] > arr[j])
    pass


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["arr"]))


if __name__ == "__main__":
    main()

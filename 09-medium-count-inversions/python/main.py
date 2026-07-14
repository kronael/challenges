import json
import sys


def solve(arr):
    pass


def main():
    obj = json.load(sys.stdin)
    arr = obj["arr"]
    if obj["n"] != len(arr):
        raise ValueError("n must match len(arr)")
    print(solve(arr))


if __name__ == "__main__":
    main()

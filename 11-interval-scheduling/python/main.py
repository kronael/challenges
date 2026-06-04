import json
import sys


def solve(intervals):
    # TODO: return the maximum number of non-overlapping intervals
    pass


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["intervals"]))


if __name__ == "__main__":
    main()

import json
import sys


def solve(k, arr):
    # TODO: return the maximum of each window of k readings, left to right
    pass


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["k"], obj["arr"]))


if __name__ == "__main__":
    main()

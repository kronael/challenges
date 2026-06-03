import json
import sys


def solve(n, initial, queries):
    # TODO: Fenwick tree — handle ["sum", i] and ["update", i, delta]
    # Return results of "sum" queries (1-indexed) in order
    pass


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["n"], obj["initial"], obj["queries"]))


if __name__ == "__main__":
    main()

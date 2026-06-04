import json
import sys


def solve(n, values, ops):
    # TODO: return the list of sum-query answers, in order
    pass


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["n"], obj["values"], obj["ops"]))


if __name__ == "__main__":
    main()

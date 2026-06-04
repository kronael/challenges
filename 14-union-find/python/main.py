import json
import sys


def solve(n, unions, queries):
    # TODO: apply unions, then return 1/0 per query for same-component
    pass


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["n"], obj["unions"], obj["queries"]))


if __name__ == "__main__":
    main()

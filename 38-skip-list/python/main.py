import json
import sys


def solve(ops):
    # TODO: skip list supporting insert/delete/search/range_count
    # Return results of "search" (1/0) and "range_count" ops in order
    pass


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["ops"]))


if __name__ == "__main__":
    main()

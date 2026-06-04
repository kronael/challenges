import json
import sys


def solve(feeds):
    # TODO: merge the K sorted feeds by ts (tie-break feed index, then id);
    # return a flat list [ts, id, ts, id, ...] in merged order
    pass


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["feeds"]))


if __name__ == "__main__":
    main()

import json
import sys


def solve(n, edges, loads):
    # TODO: return list of loads (same order as input), null ones filled in
    pass


def main():
    obj = json.load(sys.stdin)
    n = obj["n"]
    edges = [tuple(e) for e in obj["edges"]]
    loads = obj["loads"]  # int or None
    print(*solve(n, edges, loads))


if __name__ == "__main__":
    main()

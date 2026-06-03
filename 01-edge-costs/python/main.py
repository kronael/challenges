import json
import sys


def solve(n, edges, loads):
    # TODO: return list of loads with None values filled in to minimise total
    pass


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["n"], [tuple(e) for e in obj["edges"]], obj["loads"]))


if __name__ == "__main__":
    main()

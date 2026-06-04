import json
import sys


def solve(n, edges):
    # TODO: return the shortest distance from node 0 to each node, -1 if unreachable
    pass


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["n"], obj["edges"]))


if __name__ == "__main__":
    main()

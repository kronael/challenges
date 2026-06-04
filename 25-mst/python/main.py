import json
import sys


def solve(n, edges):
    # TODO: return the total weight of the minimum spanning tree
    pass


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["n"], obj["edges"]))


if __name__ == "__main__":
    main()

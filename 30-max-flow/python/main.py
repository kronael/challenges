import json
import sys


def solve(n, edges):
    # TODO: return the maximum flow from node 1 to node n
    pass


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["n"], obj["edges"]))


if __name__ == "__main__":
    main()

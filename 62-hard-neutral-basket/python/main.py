import json
import sys


def solve(n, target, exposures):
    pass


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["n"], obj["target"], obj["exposures"]))


if __name__ == "__main__":
    main()

import json
import sys


def solve(n, values, ops):
    pass


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["n"], obj["values"], obj["ops"]))


if __name__ == "__main__":
    main()

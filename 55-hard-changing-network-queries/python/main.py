import json
import sys


def solve(n, operations):
    pass


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["n"], obj["operations"]))


if __name__ == "__main__":
    main()

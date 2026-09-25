import json
import sys


def solve(n, prices):
    pass


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["n"], obj["prices"]))


if __name__ == "__main__":
    main()

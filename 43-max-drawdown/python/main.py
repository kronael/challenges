import json
import sys


def solve(prices):
    _ = prices
    pass


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["prices"]))


if __name__ == "__main__":
    main()

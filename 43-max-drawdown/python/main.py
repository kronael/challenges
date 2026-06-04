import json
import sys


def solve(prices):
    # TODO: return the maximum drawdown, max over i<j of (prices[i] - prices[j])
    pass


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["prices"]))


if __name__ == "__main__":
    main()

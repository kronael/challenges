import json
import sys


def solve(amount, coins):
    # TODO: return the minimum number of coins summing to amount, or -1 if impossible
    pass


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["amount"], obj["coins"]))


if __name__ == "__main__":
    main()

import json
import sys


def solve(amount, coins):
    pass


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["amount"], obj["coins"]))


if __name__ == "__main__":
    main()

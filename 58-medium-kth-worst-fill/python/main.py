import json
import sys


def solve(n, slippage, ks):
    pass


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["n"], obj["slippage"], obj["ks"]))


if __name__ == "__main__":
    main()

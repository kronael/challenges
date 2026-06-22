import json
import sys


def solve(n, data):
    pass


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["n"], obj["data"]))


if __name__ == "__main__":
    main()

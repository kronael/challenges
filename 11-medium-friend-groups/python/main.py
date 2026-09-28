import json
import sys


def solve(n, friendships, queries):
    pass


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["n"], obj["friendships"], obj["queries"]))


if __name__ == "__main__":
    main()

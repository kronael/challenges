import json
import sys


def solve(n, parent, queries):
    pass


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["n"], obj["parent"], obj["queries"]))


if __name__ == "__main__":
    main()

import json
import sys


def solve(n, initial, queries):
    _ = (n, initial, queries)
    pass


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["n"], obj["initial"], obj["queries"]))


if __name__ == "__main__":
    main()

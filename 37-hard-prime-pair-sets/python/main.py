import json
import sys


def solve(size, limit):
    pass


def main():
    data = json.load(sys.stdin)
    print(solve(data.get("size", 5), data.get("limit", 10000)))


if __name__ == "__main__":
    main()

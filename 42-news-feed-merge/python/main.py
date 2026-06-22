import json
import sys


def solve(feeds):
    _ = feeds
    pass


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["feeds"]))


if __name__ == "__main__":
    main()

import json
import sys


def solve(capacity, items):
    # TODO
    pass


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["capacity"], obj["items"]))


if __name__ == "__main__":
    main()

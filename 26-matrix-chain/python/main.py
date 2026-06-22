import json
import sys


def solve(dims):
    _ = dims
    pass


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["dims"]))


if __name__ == "__main__":
    main()

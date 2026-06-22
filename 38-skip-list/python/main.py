import json
import sys


def solve(ops):
    pass


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["ops"]))


if __name__ == "__main__":
    main()

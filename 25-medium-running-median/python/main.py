import json
import sys


def solve(stream):
    pass


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["stream"]))


if __name__ == "__main__":
    main()

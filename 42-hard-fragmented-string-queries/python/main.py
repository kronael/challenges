import json
import sys


def solve(parts, queries):
    _ = (parts, queries)
    pass


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["parts"], obj["queries"]))


if __name__ == "__main__":
    main()

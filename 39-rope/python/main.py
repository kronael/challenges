import json
import sys


def solve(parts, queries):
    # TODO: build a rope from parts, answer [lo, hi) substring queries
    # Return extracted substrings joined by "|"
    pass


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["parts"], obj["queries"]))


if __name__ == "__main__":
    main()

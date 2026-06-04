import json
import sys


def solve(s):
    # TODO: count the number of distinct non-empty substrings of s
    pass


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["s"]))


if __name__ == "__main__":
    main()

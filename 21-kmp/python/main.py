import json
import sys


def solve(text, pattern):
    # TODO: return the 1-indexed start positions where pattern occurs in text
    pass


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["text"], obj["pattern"]))


if __name__ == "__main__":
    main()

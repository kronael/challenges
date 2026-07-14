import json
import sys


def solve(text, pattern):
    raise NotImplementedError


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["text"], obj["pattern"]))


if __name__ == "__main__":
    main()

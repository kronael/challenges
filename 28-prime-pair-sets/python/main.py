import json
import sys


def solve(size):
    pass


def main():
    data = json.load(sys.stdin)
    print(solve(data.get("size", 5)))


if __name__ == "__main__":
    main()

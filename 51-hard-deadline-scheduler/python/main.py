import json
import sys


def solve(commands):
    pass


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["commands"]))


if __name__ == "__main__":
    main()

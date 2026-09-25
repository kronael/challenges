import json
import sys


def solve(n, links):
    pass


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["n"], obj["links"]))


if __name__ == "__main__":
    main()

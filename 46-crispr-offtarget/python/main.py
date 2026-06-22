import json
import sys


def solve(d, length, genome, guides):
    pass


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["d"], obj["len"], obj["genome"], obj["guides"]))


if __name__ == "__main__":
    main()

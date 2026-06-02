import json, sys


def solve(n, data):
    # TODO
    pass


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["n"], obj["data"]))


if __name__ == "__main__":
    main()

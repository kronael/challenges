import json
import sys


def solve(capacity, ops):
    _ = (capacity, ops)
    pass


def main():
    obj = json.load(sys.stdin)
    results = solve(obj["capacity"], obj["ops"])
    print(*results)


if __name__ == "__main__":
    main()

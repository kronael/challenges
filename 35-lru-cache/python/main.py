import json
import sys


def solve(capacity, ops):
    # TODO: LRU cache — return list of get results (-1 if miss)
    # ops: list of ["put", k, v] or ["get", k]
    pass


def main():
    obj = json.load(sys.stdin)
    results = solve(obj["capacity"], obj["ops"])
    print(*results)


if __name__ == "__main__":
    main()

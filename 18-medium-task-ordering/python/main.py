import json
import sys


def solve(n, edges):
    _ = (n, edges)
    pass


def main():
    obj = json.load(sys.stdin)
    res = solve(obj["n"], obj["edges"])
    if res == "CYCLE":
        print("CYCLE")
    else:
        print(*res)


if __name__ == "__main__":
    main()

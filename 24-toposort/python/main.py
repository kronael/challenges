import json
import sys


def solve(n, edges):
    # TODO: return a list giving a valid topological order (smallest ready node
    # first), or the string "CYCLE" if no ordering exists
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

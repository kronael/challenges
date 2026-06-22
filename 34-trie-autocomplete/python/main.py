import json
import sys


def solve(words, queries):
    # Join query results with ";", and words inside one result with " ".
    pass


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["words"], obj["queries"]))


if __name__ == "__main__":
    main()

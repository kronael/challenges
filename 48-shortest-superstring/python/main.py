import json
import sys


def solve(reads):
    # TODO: return the shortest superstring containing every read (the reassembled chromosome)
    pass


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["reads"]))


if __name__ == "__main__":
    main()

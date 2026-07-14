import bisect
import json
import sys


def solve(seq):
    tails = []
    for x in seq:
        i = bisect.bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["seq"]))


if __name__ == "__main__":
    main()

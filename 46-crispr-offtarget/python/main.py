import json
import sys


def solve(d, length, genome, guides):
    # TODO: for each guide, count the length-`length` windows of `genome` within
    # Hamming distance `d` of it. Return one count per guide, in input order.
    pass


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["d"], obj["len"], obj["genome"], obj["guides"]))


if __name__ == "__main__":
    main()

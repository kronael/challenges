import itertools
import json
import sys


def solve(costs):
    # Naive: try all n! one-to-one placements and keep the cheapest total.
    # Correct, but factorial work TIMEOUTs on the 12x12 and 13x13 large cases.
    best = None
    for hosts in itertools.permutations(range(len(costs))):
        total = sum(costs[service][host] for service, host in enumerate(hosts))
        if best is None or total < best:
            best = total
    return best


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["costs"]))


if __name__ == "__main__":
    main()

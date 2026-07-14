import json
import sys


def solve(jobs):
    # jobs: list of (start, end, weight) tuples
    pass


def main():
    obj = json.load(sys.stdin)
    jobs = [(j["start"], j["end"], j["weight"]) for j in obj["jobs"]]
    print(solve(jobs))


if __name__ == "__main__":
    main()

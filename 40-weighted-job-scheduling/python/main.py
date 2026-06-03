import json, sys


def solve(jobs):
    # jobs: list of (start, end, weight) tuples
    # TODO: return maximum total weight of non-overlapping jobs
    pass


def main():
    obj = json.load(sys.stdin)
    jobs = [(j["start"], j["end"], j["weight"]) for j in obj["jobs"]]
    print(solve(jobs))


if __name__ == "__main__":
    main()

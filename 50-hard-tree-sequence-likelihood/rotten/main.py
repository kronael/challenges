import itertools
import json
import math
import sys

BASE_INDEX = {"A": 0, "C": 1, "G": 2, "T": 3}


def solve(parent, sequences, prior, transition):
    # Naive: enumerate all 4^i base assignments for the i internal nodes.
    # Correct, but exponential work TIMEOUTs on the 15-internal-node large trees.
    internal = [node for node, sequence in enumerate(sequences) if sequence is None]
    site_count = len(next(sequence for sequence in sequences if sequence is not None))
    total_log_likelihood = 0.0

    for site in range(site_count):
        states = [0] * len(parent)
        for node, sequence in enumerate(sequences):
            if sequence is not None:
                states[node] = BASE_INDEX[sequence[site]]

        site_likelihood = 0.0
        for assignment in itertools.product(range(4), repeat=len(internal)):
            for node, state in zip(internal, assignment, strict=True):
                states[node] = state
            probability = prior[states[0]]
            for node in range(1, len(parent)):
                probability *= transition[states[parent[node]]][states[node]]
            site_likelihood += probability
        total_log_likelihood += math.log(site_likelihood)

    return total_log_likelihood


def main():
    obj = json.load(sys.stdin)
    result = solve(
        obj["parent"],
        obj["sequences"],
        obj["prior"],
        obj["transition"],
    )
    print(f"{result:.6f}")


if __name__ == "__main__":
    main()

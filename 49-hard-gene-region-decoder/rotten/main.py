import itertools
import json
import sys

BASE_INDEX = {"A": 0, "C": 1, "G": 2, "T": 3}


def solve(sequence, start, transition, emission):
    # Naive: enumerate all k^n complete state paths and score each one.
    # Correct, but exponential work TIMEOUTs on the 28-base large cases.
    state_count = len(start)
    best_path = None
    best_score = None
    for path in itertools.product(range(state_count), repeat=len(sequence)):
        score = start[path[0]] + emission[path[0]][BASE_INDEX[sequence[0]]]
        for position in range(1, len(sequence)):
            score += transition[path[position - 1]][path[position]]
            score += emission[path[position]][BASE_INDEX[sequence[position]]]
        if best_score is None or score > best_score:
            best_path = path
            best_score = score
    return best_path


def main():
    obj = json.load(sys.stdin)
    print(
        *solve(
            obj["sequence"],
            obj["start"],
            obj["transition"],
            obj["emission"],
        )
    )


if __name__ == "__main__":
    main()

import json
import sys

BASE_INDEX = {"A": 0, "C": 1, "G": 2, "T": 3}


def solve(sequence, start, transition, emission):
    state_count = len(start)
    bases = [BASE_INDEX[base] for base in sequence]
    previous = [start[state] + emission[state][bases[0]] for state in range(state_count)]
    back = [[0] * state_count for _ in sequence]

    for position in range(1, len(sequence)):
        current = [0] * state_count
        for state in range(state_count):
            best_previous = 0
            best_score = previous[0] + transition[0][state]
            for candidate in range(1, state_count):
                score = previous[candidate] + transition[candidate][state]
                if score > best_score:
                    best_previous = candidate
                    best_score = score
            current[state] = best_score + emission[state][bases[position]]
            back[position][state] = best_previous
        previous = current

    final_state = max(range(state_count), key=previous.__getitem__)
    path = [0] * len(sequence)
    path[-1] = final_state
    for position in range(len(sequence) - 1, 0, -1):
        path[position - 1] = back[position][path[position]]
    return path


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

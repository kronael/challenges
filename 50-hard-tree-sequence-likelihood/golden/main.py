import json
import math
import sys

BASE_INDEX = {"A": 0, "C": 1, "G": 2, "T": 3}


def log_sum_exp(values):
    maximum = max(values)
    return maximum + math.log(sum(math.exp(value - maximum) for value in values))


def solve(parent, sequences, prior, transition):
    children = [[] for _ in parent]
    for node in range(1, len(parent)):
        children[parent[node]].append(node)

    log_prior = [math.log(value) for value in prior]
    log_transition = [[math.log(value) for value in row] for row in transition]
    site_count = len(next(sequence for sequence in sequences if sequence is not None))
    total = 0.0

    for site in range(site_count):
        likelihood = [[0.0] * 4 for _ in parent]
        for node in range(len(parent) - 1, -1, -1):
            sequence = sequences[node]
            if sequence is not None:
                observed = BASE_INDEX[sequence[site]]
                likelihood[node] = [
                    0.0 if state == observed else -math.inf for state in range(4)
                ]
                continue

            for state in range(4):
                subtotal = 0.0
                for child in children[node]:
                    subtotal += log_sum_exp(
                        [
                            log_transition[state][child_state]
                            + likelihood[child][child_state]
                            for child_state in range(4)
                        ]
                    )
                likelihood[node][state] = subtotal

        total += log_sum_exp(
            [log_prior[state] + likelihood[0][state] for state in range(4)]
        )
    return total


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

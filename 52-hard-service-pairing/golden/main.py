import json
import sys


def solve(costs):
    size = len(costs)
    row_potential = [0] * (size + 1)
    column_potential = [0] * (size + 1)
    matched_row = [0] * (size + 1)
    previous_column = [0] * (size + 1)

    for row in range(1, size + 1):
        matched_row[0] = row
        minimum_slack = [None] + [sys.maxsize] * size
        used = [False] * (size + 1)
        column = 0

        while True:
            used[column] = True
            current_row = matched_row[column]
            delta = sys.maxsize
            next_column = 0
            for candidate in range(1, size + 1):
                if used[candidate]:
                    continue
                reduced_cost = (
                    costs[current_row - 1][candidate - 1]
                    - row_potential[current_row]
                    - column_potential[candidate]
                )
                if reduced_cost < minimum_slack[candidate]:
                    minimum_slack[candidate] = reduced_cost
                    previous_column[candidate] = column
                if minimum_slack[candidate] < delta:
                    delta = minimum_slack[candidate]
                    next_column = candidate

            for candidate in range(size + 1):
                if used[candidate]:
                    row_potential[matched_row[candidate]] += delta
                    column_potential[candidate] -= delta
                elif candidate > 0:
                    minimum_slack[candidate] -= delta

            column = next_column
            if matched_row[column] == 0:
                break

        while True:
            prior = previous_column[column]
            matched_row[column] = matched_row[prior]
            column = prior
            if column == 0:
                break

    return -column_potential[0]


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["costs"]))


if __name__ == "__main__":
    main()

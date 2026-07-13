import json
import sys


def is_prime(x):
    if x < 2:
        return False
    i = 2
    while i * i <= x:
        if x % i == 0:
            return False
        i += 1
    return True


def solve(n):
    # Naive O(n*sqrt(n)) trial division: correct, but TIMEOUTs on the large
    # cases — the trap.
    count = 0
    for x in range(2, n):
        if is_prime(x):
            count += 1
    return count


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["n"]))


if __name__ == "__main__":
    main()

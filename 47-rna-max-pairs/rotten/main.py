import json
import sys


def can_pair(a, b, allow_wobble):
    pairs = {"AU", "UA", "CG", "GC"}
    if allow_wobble:
        pairs |= {"GU", "UG"}
    return a + b in pairs


def solve(rna, min_loop, allow_wobble):
    # Naive exponential recursion with NO memoization: correct, but the branching
    # over every possible partner for each base blows up — TIMEOUTs on the large
    # cases. The trap.
    def best(i, j):
        if i >= j:
            return 0
        # rightmost base j unpaired
        r = best(i, j - 1)
        # j pairs with some k in [i, j), splitting the interval
        for k in range(i, j):
            if j - k > min_loop and can_pair(rna[k], rna[j], allow_wobble):
                left = best(i, k - 1) if k > i else 0
                r = max(r, left + 1 + best(k + 1, j - 1))
        return r

    n = len(rna)
    return best(0, n - 1) if n > 0 else 0


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["rna"], obj["min_loop"], obj["allow_wobble"]))


if __name__ == "__main__":
    main()

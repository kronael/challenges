import json
import sys


def solve(d, length, genome, guides):
    # Naive triple loop: each guide x each window x each base. Correct, but
    # O(guides * genome * length) — it TIMEOUTs on the large cases. The trap.
    n = len(genome)
    out = []
    for g in guides:
        count = 0
        for s in range(n - length + 1):
            mism = 0
            for i in range(length):
                if genome[s + i] != g[i]:
                    mism += 1
            if mism <= d:
                count += 1
        out.append(count)
    return out


def main():
    obj = json.load(sys.stdin)
    print(*solve(obj["d"], obj["len"], obj["genome"], obj["guides"]))


if __name__ == "__main__":
    main()

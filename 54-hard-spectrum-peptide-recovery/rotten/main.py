import json
import sys


def cyclic_spectrum(peptide):
    prefix = [0]
    for mass in peptide:
        prefix.append(prefix[-1] + mass)
    total = prefix[-1]
    spectrum = [0]
    for start in range(len(peptide)):
        for end in range(start + 1, len(peptide) + 1):
            mass = prefix[end] - prefix[start]
            spectrum.append(mass)
            if start > 0 and end < len(peptide):
                spectrum.append(total - mass)
    return sorted(spectrum)


def solve(masses, spectrum):
    parent = spectrum[-1]
    matches = []

    # Naive: enumerate every mass sequence whose sum can reach the parent, then
    # build its full spectrum. Correct, but exponential branching TIMEOUTs.
    def visit(peptide, total):
        if total == parent:
            if cyclic_spectrum(peptide) == spectrum:
                matches.append(peptide)
            return
        for mass in masses:
            if total + mass <= parent:
                visit(peptide + [mass], total + mass)

    visit([], 0)
    return min(matches, default=None)


def main():
    obj = json.load(sys.stdin)
    result = solve(obj["masses"], obj["spectrum"])
    print("NONE" if result is None else " ".join(map(str, result)))


if __name__ == "__main__":
    main()

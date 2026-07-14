import json
import sys
from collections import Counter


def linear_spectrum(peptide):
    prefix = [0]
    for mass in peptide:
        prefix.append(prefix[-1] + mass)
    spectrum = [0]
    for start in range(len(peptide)):
        for end in range(start + 1, len(peptide) + 1):
            spectrum.append(prefix[end] - prefix[start])
    return spectrum


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
    target = sorted(spectrum)
    target_counts = Counter(target)
    parent = target[-1]
    candidates = [()]
    matches = []
    while candidates:
        next_candidates = []
        for candidate in candidates:
            for mass in masses:
                peptide = candidate + (mass,)
                total = sum(peptide)
                if total == parent:
                    if cyclic_spectrum(peptide) == target:
                        matches.append(peptide)
                elif total < parent:
                    counts = Counter(linear_spectrum(peptide))
                    if all(
                        count <= target_counts[value] for value, count in counts.items()
                    ):
                        next_candidates.append(peptide)
        candidates = next_candidates
    return list(min(matches)) if matches else None


def main():
    obj = json.load(sys.stdin)
    result = solve(obj["masses"], obj["spectrum"])
    print("NONE" if result is None else " ".join(map(str, result)))


if __name__ == "__main__":
    main()

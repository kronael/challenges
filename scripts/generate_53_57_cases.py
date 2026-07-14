#!/usr/bin/env python3
"""Generate deterministic inputs for challenges 53 through 57."""

import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def write(challenge, name, data):
    path = ROOT / challenge / "cases" / f"{name}.in"
    path.write_text(json.dumps(data, separators=(",", ":")) + "\n")


def genome_cases():
    challenge = "53-hard-circular-genome-distance"
    cases = [
        ("01", {"a": [[1]], "b": [[1]]}),
        ("02", {"a": [[1]], "b": [[-1]]}),
        ("03", {"a": [[1, 2, 3]], "b": [[-3, -2, -1]]}),
        ("04", {"a": [[1, 2, 3, 4]], "b": [[1, -2, 3, 4]]}),
        ("05", {"a": [[1, 2], [3, 4]], "b": [[1, 2, 3, 4]]}),
        ("06", {"a": [[1, 2, 3, 4, 5, 6]], "b": [[1, -3, -6, -5, 2, 4]]}),
        (
            "07",
            {
                "a": [[1, -2, 3], [4, 5], [-6, 7, 8]],
                "b": [[1, 8, -7], [2, -3, 4, 5, 6]],
            },
        ),
        (
            "08",
            {
                "a": [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]],
                "b": [[1, -4, 7, 10], [2, 5, -8], [3, 6, 9]],
            },
        ),
    ]
    for name, data in cases:
        write(challenge, name, data)

    n = 40000
    blocks = list(range(1, n + 1))
    write(challenge, "09_large_same", {"a": [blocks], "b": [blocks]})
    write(challenge, "10_large_singletons", {"a": [blocks], "b": [[x] for x in blocks]})


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


def peptide_cases():
    challenge = "54-hard-spectrum-peptide-recovery"
    planted = [
        ("01", [57, 71], [57]),
        ("02", [57, 71], [57, 71]),
        ("03", [113, 128, 186], [113, 128, 186]),
        ("04", [57, 71], [57, 57, 71]),
        ("05", [71, 87, 97, 101], [71, 87, 97, 101]),
        ("07", [57, 71, 87], [87, 57, 71]),
        ("08", [57, 71, 87], [57, 71, 57, 87, 71]),
    ]
    for name, masses, peptide in planted:
        write(challenge, name, {"masses": masses, "spectrum": cyclic_spectrum(peptide)})
    write(challenge, "06", {"masses": [57, 71], "spectrum": [0, 58]})

    masses = [57, 71, 87, 97, 99, 101]
    peptide = [57, 71, 87, 97, 99, 101, 57, 87, 71, 97]
    write(
        challenge,
        "09_large_six_masses",
        {"masses": masses, "spectrum": cyclic_spectrum(peptide)},
    )
    masses = [57, 71, 87, 97, 99, 101, 103]
    peptide = [103, 57, 71, 99, 87, 101, 97, 57, 103, 71, 87]
    write(
        challenge,
        "10_large_seven_masses",
        {"masses": masses, "spectrum": cyclic_spectrum(peptide)},
    )


def op(kind, u, v):
    return {"type": kind, "u": u, "v": v}


def network_cases():
    challenge = "55-hard-changing-network-queries"
    cases = [
        ("01", 1, [op("ask", 0, 0)]),
        ("02", 3, [op("ask", 0, 2)]),
        ("03", 3, [op("add", 0, 1), op("ask", 0, 1), op("ask", 0, 2)]),
        ("04", 3, [op("add", 0, 1), op("remove", 0, 1), op("ask", 0, 1)]),
        (
            "05",
            5,
            [
                op("add", 0, 1),
                op("add", 1, 2),
                op("add", 2, 3),
                op("ask", 0, 3),
                op("remove", 1, 2),
                op("ask", 0, 3),
            ],
        ),
        (
            "06",
            4,
            [
                op("add", 0, 1),
                op("add", 1, 2),
                op("add", 2, 0),
                op("remove", 0, 1),
                op("ask", 0, 1),
            ],
        ),
        (
            "07",
            3,
            [
                op("add", 0, 1),
                op("ask", 0, 1),
                op("remove", 0, 1),
                op("add", 0, 1),
                op("ask", 0, 1),
            ],
        ),
        (
            "08",
            8,
            [op("add", 0, i) for i in range(1, 8)]
            + [op("ask", 1, 7), op("remove", 0, 4), op("ask", 4, 7)],
        ),
    ]
    for name, n, operations in cases:
        write(challenge, name, {"n": n, "operations": operations})

    n = 15000
    operations = [op("add", i, i + 1) for i in range(n - 1)]
    operations += [op("ask", 0, n - 1) for _ in range(n)]
    write(challenge, "09_large_path", {"n": n, "operations": operations})

    n = 12000
    operations = [op("add", 0, i) for i in range(1, n)]
    operations += [op("ask", 1, n - 1) for _ in range(n)]
    write(challenge, "10_large_star", {"n": n, "operations": operations})


def crossing_cases():
    challenge = "56-hard-orthogonal-segment-crossings"
    cases = [
        ("01", [], []),
        ("02", [[0, 2, 1]], [[1, 0, 2]]),
        ("03", [[0, 2, 1]], [[2, 1, 3]]),
        ("04", [[0, 1, 0]], [[2, -1, 1]]),
        ("05", [[0, 4, 2], [0, 4, 2]], [[2, 0, 4], [2, 2, 2]]),
        ("06", [[-5, -1, -3], [-4, 3, 0]], [[-4, -5, 1], [0, -1, 4]]),
        ("07", [[0, 10, y] for y in range(4)], [[x, 0, 3] for x in range(5)]),
        ("08", [[i, i + 8, i] for i in range(8)], [[i + 4, 0, 8] for i in range(8)]),
    ]
    for name, horizontal, vertical in cases:
        write(challenge, name, {"horizontal": horizontal, "vertical": vertical})

    n = 20000
    horizontal = [[0, n, y] for y in range(n)]
    vertical = [[x, 0, n - 1] for x in range(n)]
    write(challenge, "09_large_dense", {"horizontal": horizontal, "vertical": vertical})

    n = 25000
    horizontal = [[3 * i, 3 * i + 1, i] for i in range(n)]
    vertical = [[3 * i + 2, 0, n - 1] for i in range(n)]
    write(
        challenge, "10_large_sparse", {"horizontal": horizontal, "vertical": vertical}
    )


def event(event_id, process, clock):
    return {"id": event_id, "process": process, "clock": clock}


def replay_cases():
    challenge = "57-hard-causal-event-replay"
    cases = [
        ("01", 1, [event(5, 0, [1])]),
        ("02", 2, [event(20, 1, [0, 1]), event(10, 0, [1, 0])]),
        ("03", 1, [event(30, 0, [3]), event(10, 0, [1]), event(20, 0, [2])]),
        ("04", 2, [event(30, 1, [1, 1]), event(10, 0, [1, 0]), event(20, 0, [2, 0])]),
        ("05", 2, [event(40, 0, [2, 1]), event(15, 1, [0, 1]), event(10, 0, [1, 0])]),
        (
            "06",
            3,
            [event(30, 2, [1, 1, 1]), event(20, 1, [1, 1, 0]), event(10, 0, [1, 0, 0])],
        ),
        (
            "07",
            3,
            [
                event(40, 2, [1, 1, 2]),
                event(30, 1, [0, 1, 0]),
                event(20, 0, [1, 0, 0]),
                event(10, 2, [0, 0, 1]),
            ],
        ),
        (
            "08",
            4,
            [
                event(80, 3, [2, 1, 1, 2]),
                event(30, 2, [0, 0, 1, 0]),
                event(10, 0, [1, 0, 0, 0]),
                event(40, 3, [0, 0, 0, 1]),
                event(20, 1, [0, 1, 0, 0]),
                event(70, 0, [2, 1, 1, 1]),
            ],
        ),
    ]
    for name, processes, events in cases:
        write(challenge, name, {"processes": processes, "events": events})

    rng = random.Random(5709)
    processes = 4
    events = []
    for process in range(processes):
        for sequence in range(1, 5001):
            clock = [0] * processes
            clock[process] = sequence
            events.append(event(rng.randrange(1, 10**9), process, clock))
    ids = rng.sample(range(1, 10**9), len(events))
    for item, event_id in zip(events, ids):
        item["id"] = event_id
    rng.shuffle(events)
    write(challenge, "09_large_independent", {"processes": processes, "events": events})

    rng = random.Random(5710)
    processes = 4
    counts = [0] * processes
    events = []
    ids = rng.sample(range(1, 10**9), 20000)
    for i in range(20000):
        process = i % processes
        counts[process] += 1
        events.append(event(ids[i], process, counts.copy()))
    rng.shuffle(events)
    write(challenge, "10_large_chain", {"processes": processes, "events": events})


def main():
    genome_cases()
    peptide_cases()
    network_cases()
    crossing_cases()
    replay_cases()


if __name__ == "__main__":
    main()

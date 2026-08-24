"""Build deterministic large benchmark inputs from small checked-in recipes."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, TextIO

MASK_64 = (1 << 64) - 1
DNA = "ACGT"
LOWER = "abcdefghijklmnopqrstuvwxyz"
PROTEIN = "ARNDCQEGHILKMFPSTWYV"
RNA = "ACGU"
EXPECTED_DIGEST = "d6592d33ee68c34f8c107c9f7d26aa5f36d7b11033d050ef6e42226a0857b75e"


class Rng:
    """Small, version-independent SplitMix64 generator."""

    def __init__(self, seed: int) -> None:
        self.state = seed & MASK_64

    def next(self) -> int:
        self.state = (self.state + 0x9E3779B97F4A7C15) & MASK_64
        value = self.state
        value = ((value ^ (value >> 30)) * 0xBF58476D1CE4E5B9) & MASK_64
        value = ((value ^ (value >> 27)) * 0x94D049BB133111EB) & MASK_64
        return value ^ (value >> 31)

    def integer(self, low: int, high: int) -> int:
        return low + self.next() % (high - low + 1)

    def text(self, alphabet: str, length: int) -> str:
        return "".join(alphabet[self.next() % len(alphabet)] for _ in range(length))

    def shuffle(self, values: list[Any]) -> None:
        for i in range(len(values) - 1, 0, -1):
            j = self.next() % (i + 1)
            values[i], values[j] = values[j], values[i]


@dataclass(frozen=True, slots=True)
class Case:
    challenge: str
    name: str
    seed: int
    repeats: int = 1


def build_01(name: str, rng: Rng) -> dict[str, Any]:
    if name == "09_large_random":
        return {"arr": [rng.integer(-1000, 1000) for _ in range(1_000_000)]}
    return {"arr": [rng.integer(-1000, -1) for _ in range(1_000_000)]}


def build_02(name: str, rng: Rng) -> dict[str, Any]:
    del rng
    if name == "09_large_exp":
        return {"base": 2, "exp": 10**18, "mod": 1_000_000_007}
    return {"base": 10**18, "exp": 10**18, "mod": 998_244_353}


def build_03(name: str, rng: Rng) -> dict[str, Any]:
    n = 200_000
    if name == "09_large_decline":
        prices = [1_000_000 - 6 * i for i in range(n)]
    else:
        price = 500_000
        prices = []
        for _ in range(n):
            price += rng.integer(-50, 50)
            prices.append(price)
    return {"n": n, "prices": prices}


def build_04(name: str, rng: Rng) -> dict[str, Any]:
    del rng
    if name == "09_large_path":
        n = 200_001
        edges = [[i, i + 1] for i in range(n - 1)]
        loads = [None] * n
        loads[n // 2] = 100_000
    elif name == "10_large_star":
        n = 100_001
        edges = [[0, i] for i in range(1, n)]
        loads = [None] * n
        loads[1] = 500
    else:
        n = 100_000
        edges = [[i, i + 1] for i in range(49_999)]
        edges.extend([i, i + 50_000] for i in range(50_000))
        loads = [None] * n
        loads[0] = 80_000
    return {"n": n, "edges": edges, "loads": loads}


def build_05(name: str, rng: Rng) -> dict[str, Any]:
    n = 200_000
    if name == "09_large_increasing":
        seq = list(range(n))
    else:
        seq = [rng.integer(0, 1_000_000_000) for _ in range(n)]
    return {"n": n, "seq": seq}


def build_06(name: str, rng: Rng) -> dict[str, Any]:
    alphabet = LOWER if name == "09_large_random" else "ab"
    length = 3_000 if name == "09_large_random" else 4_000
    return {
        "s": rng.text(alphabet, length),
        "t": rng.text(alphabet, length),
    }


def build_07(name: str, rng: Rng) -> dict[str, Any]:
    del rng
    if name == "09_large_amount":
        return {"amount": 1_000_000, "coins": [1, 7, 23, 101, 211, 307, 503]}
    return {"amount": 2_000_000, "coins": [3, 5, 7, 11]}


def build_08(name: str, rng: Rng) -> dict[str, Any]:
    n = 200_000
    if name == "09_large_random":
        intervals = []
        for _ in range(n):
            start = rng.integer(0, 1_000_000_000)
            intervals.append([start, start + rng.integer(1, 1_000)])
    else:
        intervals = [[i, i + 1] for i in range(n)]
    return {"n": n, "intervals": intervals}


def build_09(name: str, rng: Rng) -> dict[str, Any]:
    n = 200_000
    if name == "09_large_reversed":
        arr = list(range(2 * n, n, -1))
    else:
        arr = [rng.integer(-(1 << 30), (1 << 30) - 1) for _ in range(n)]
    return {"n": n, "arr": arr}


def build_10(name: str, rng: Rng) -> dict[str, Any]:
    if name == "09_large_sparse":
        n = 100_000
        edges = [[i, i + 1, rng.integer(1, 1_000)] for i in range(n - 1)]
        while len(edges) < 400_000:
            u = rng.integer(0, n - 1)
            v = rng.integer(0, n - 1)
            if u != v:
                edges.append([u, v, rng.integer(1, 1_000)])
    else:
        n = 200_000
        edges = [[i, i + 1, rng.integer(1, 100)] for i in range(n - 1)]
    return {"n": n, "edges": edges}


def build_11(name: str, rng: Rng) -> dict[str, Any]:
    n = 200_000
    if name == "09_large_random":
        unions = [
            [rng.integer(0, n - 1), rng.integer(0, n - 1)] for _ in range(n)
        ]
        queries = [
            [rng.integer(0, n - 1), rng.integer(0, n - 1)] for _ in range(n)
        ]
    else:
        unions = [[i, i + 1] for i in range(n - 1)]
        queries = [[0, rng.integer(0, n - 1)] for _ in range(n)]
    return {"n": n, "unions": unions, "queries": queries}


def build_12(name: str, rng: Rng) -> dict[str, Any]:
    if name == "09_large_random":
        return {"k": 500, "pages": [rng.integer(1, 10_000) for _ in range(200_000)]}
    return {
        "k": 12_345,
        "pages": [rng.integer(1, 1_000_000) for _ in range(200_000)],
    }


def build_13(name: str, rng: Rng) -> dict[str, Any]:
    n = 200_000
    if name == "09_large_random":
        arr = [rng.integer(-1_000_000_000, 1_000_000_000) for _ in range(n)]
    else:
        arr = list(range(n, 0, -1))
    return {"k": 50_000, "arr": arr}


def build_14(name: str, rng: Rng) -> dict[str, Any]:
    del rng
    return {"n": 10_000_000 if name == "09_large_ten_million" else 100_000_000}


def build_15(name: str, rng: Rng) -> dict[str, Any]:
    del rng
    return {"n": 10**18 if name == "09_large_n" else 999_999_999_999_999_937}


def build_16(name: str, rng: Rng) -> dict[str, Any]:
    del rng
    pattern = "a" * 12_000
    if name == "09_large_allmatch":
        text = "a" * 2_500_000
    else:
        pattern = "a" * 11_999 + "b"
        text = "a" * 2_500_000
    return {"text": text, "pattern": pattern}


def build_17(name: str, rng: Rng) -> dict[str, Any]:
    if name == "09_large_random":
        items = [
            {"weight": rng.integer(1, 1_000), "value": rng.integer(1, 1_000)}
            for _ in range(1_000)
        ]
    else:
        items = [
            {"weight": rng.integer(1, 50), "value": rng.integer(1, 100)}
            for _ in range(1_000)
        ]
    return {"capacity": 10_000, "items": items}


def build_18(name: str, rng: Rng) -> dict[str, Any]:
    n = 200_000
    if name == "10_large_path":
        return {"n": n, "edges": [[i, i - 1] for i in range(n - 1, 0, -1)]}

    edges = [[i, i + 1] for i in range(n - 1)]
    if name == "09_large_dag":
        while len(edges) < 400_000:
            u = rng.integer(0, n - 2)
            v = rng.integer(u + 1, n - 1)
            edges.append([u, v])
        rng.shuffle(edges)
    return {"n": n, "edges": edges}


def build_19(name: str, rng: Rng) -> dict[str, Any]:
    n = 10_000
    edges = [[i, i + 1, rng.integer(1, 1_000)] for i in range(n - 1)]
    target = 200_000 if name == "09_large_random" else 300_000
    while len(edges) < target:
        u = rng.integer(0, n - 1)
        v = rng.integer(0, n - 1)
        if u != v:
            weight = rng.integer(1, 1_000_000)
            edges.append([u, v, weight])
    if name == "09_large_random":
        rng.shuffle(edges)
    return {"n": n, "edges": edges}


def build_20(name: str, rng: Rng) -> dict[str, Any]:
    alphabet = DNA if name == "09_large_dna" else "ab"
    return {"s": rng.text(alphabet, 3_000), "t": rng.text(alphabet, 3_000)}


def encode_word(value: int, length: int) -> str:
    chars = ["a"] * length
    for i in range(length - 1, -1, -1):
        chars[i] = LOWER[value % len(LOWER)]
        value //= len(LOWER)
    return "".join(chars)


def build_23(name: str, rng: Rng) -> dict[str, Any]:
    if name == "09_large_dense":
        words = ["aaaa" + encode_word(i, 6) for i in range(50_000)]
        queries = ["a" * rng.integer(1, 4) for _ in range(100_000)]
    else:
        words = [encode_word(i, 5) + rng.text(LOWER, 15) for i in range(50_000)]
        queries = [rng.text(LOWER, rng.integer(1, 3)) for _ in range(100_000)]
    return {"words": words, "queries": queries}


def build_24(name: str, rng: Rng) -> dict[str, Any]:
    capacity = 100_000
    if name == "09_large_mixed":
        ops = []
        for i in range(400_000):
            key = rng.integer(0, 199_999)
            if i % 3 == 0:
                ops.append(["get", key])
            else:
                ops.append(["put", key, rng.integer(0, 1_000_000_000)])
    else:
        # A monotone key frontier keeps the cache full, so nearly every put evicts.
        # Gets probe a random distance behind the frontier, straddling the resident
        # window: a hit also refreshes recency and changes who is evicted next, so
        # the answer pins the eviction order rather than only the running time.
        ops = []
        for i in range(400_000):
            if i % 4 == 3:
                ops.append(["get", i - 1 - rng.integer(0, 149_999) % i])
            else:
                ops.append(["put", i, rng.integer(0, 1_000_000_000)])
    return {"capacity": capacity, "ops": ops}


def build_25(name: str, rng: Rng) -> dict[str, Any]:
    if name == "09_large_random":
        stream = [rng.integer(-1_000_000, 1_000_000) for _ in range(200_000)]
    else:
        stream = list(range(-1_000_000, 1_000_000, 10))
    return {"stream": stream}


def build_26(name: str, rng: Rng) -> dict[str, Any]:
    n = 300_000
    initial = [rng.integer(-1_000, 1_000) for _ in range(n)]
    if name == "09_large_mixed":
        queries = []
        for i in range(n):
            if i % 2 == 0:
                queries.append(["update", rng.integer(1, n), rng.integer(-1_000, 1_000)])
            else:
                queries.append(["sum", n])
    else:
        queries = [["sum", n] for _ in range(n)]
    return {"n": n, "initial": initial, "queries": queries}


def build_27(name: str, rng: Rng) -> dict[str, Any]:
    if name == "09_large_random":
        jobs = []
        for i in range(100_000):
            start = i * 3
            jobs.append(
                {
                    "start": start,
                    "end": start + rng.integer(1, 100),
                    "weight": rng.integer(1, 1_000),
                }
            )
    else:
        jobs = [
            {"start": i, "end": i + 1, "weight": i % 1_000 + 1}
            for i in range(100_000)
        ]
    return {"jobs": jobs}


def build_28(name: str, rng: Rng) -> dict[str, Any]:
    del rng
    feed_count = 20_000
    next_id = 1
    feeds = []
    if name == "09_large_many":
        for feed in range(feed_count):
            items = []
            for item in range(25):
                items.append({"ts": item * feed_count + feed, "id": next_id})
                next_id += 1
            feeds.append(items)
    else:
        feeds.append([{"ts": 2 * i, "id": i + 1} for i in range(100_000)])
        next_id = 100_001
        for feed in range(1, feed_count):
            items = []
            for item in range(20):
                items.append(
                    {"ts": 2 * (item * (feed_count - 1) + feed - 1) + 1, "id": next_id}
                )
                next_id += 1
            feeds.append(items)
    return {"feeds": feeds}


def build_35(name: str, rng: Rng) -> dict[str, Any]:
    n = 300_000
    values = [rng.integer(-1_000, 1_000) for _ in range(n)]
    updates = [
        ["update", rng.integer(1, n // 16), rng.integer(-1_000, 1_000)]
        for _ in range(n // 2)
    ]
    queries = [
        ["sum", rng.integer(1, n // 4), rng.integer(3 * n // 4, n)]
        for _ in range(n // 2)
    ]
    if name == "09_large_mixed":
        ops = [op for pair in zip(updates, queries, strict=True) for op in pair]
    else:
        ops = updates + queries
    return {"n": n, "values": values, "ops": ops}


def build_36(name: str, rng: Rng) -> dict[str, Any]:
    low = 1 if name == "09_large_random" else 50
    return {"dims": [rng.integer(low, 100) for _ in range(501)]}


def build_37(name: str, rng: Rng) -> dict[str, Any]:
    del rng
    return {"size": 5, "limit": 10_000 if name == "09_large_full" else 12_000}


def build_38(name: str, rng: Rng) -> dict[str, Any]:
    alphabet = LOWER if name == "09_large_random" else "ab"
    return {"s": rng.text(alphabet, 100_000)}


def build_39(name: str, rng: Rng) -> dict[str, Any]:
    if name == "10_large_parallel":
        return {"n": 2, "edges": [[1, 2, 1] for _ in range(200_000)]}
    n = 500
    edges = []
    while len(edges) < 2_000:
        u = rng.integer(1, n - 1)
        v = rng.integer(2, n)
        if u != v:
            edges.append([u, v, rng.integer(1, 1_000_000_000)])
    return {"n": n, "edges": edges}


def build_41(name: str, rng: Rng) -> dict[str, Any]:
    if name == "09_large_search":
        values = [rng.integer(-(1 << 31), (1 << 31) - 1) for _ in range(200_000)]
        ops = [["insert", value] for value in values]
        ops.extend(
            ["search", rng.integer(-(1 << 31), (1 << 31) - 1)]
            for _ in range(200_000)
        )
    else:
        values = [rng.integer(-2_000_000, 2_000_000) for _ in range(125_000)]
        ops = [["insert", value] for value in values]
        if name == "10_large_range":
            for _ in range(125_000):
                low = rng.integer(-2_000_000, 1_990_000)
                ops.append(["range_count", low, low + rng.integer(0, 10_000)])
        else:
            ops.extend(
                ["range_count", -(1 << 31), (1 << 31) - 1]
                for _ in range(125_000)
            )
    return {"ops": ops}


def build_42(name: str, rng: Rng) -> dict[str, Any]:
    part_count = 30_000 if name == "09_large_windows" else 20_000
    parts = [rng.text(LOWER, 100) for _ in range(part_count)]
    total = part_count * 100
    width = 100 if name == "09_large_windows" else 1_000
    queries = []
    for _ in range(10_000):
        start = rng.integer(0, total)
        queries.append([start, min(total, start + rng.integer(0, width))])
    return {"parts": parts, "queries": queries}


def build_43(name: str, rng: Rng) -> dict[str, Any]:
    if name == "09_large_deep_book":
        orders = []
        buy_count = 0
        while len(orders) < 200_000:
            if len(orders) % 11 == 10:
                orders.append(
                    {"side": "sell", "price": 950_001, "qty": 7, "type": "limit"}
                )
            else:
                orders.append(
                    {
                        "side": "buy",
                        "price": 1_000_000 - buy_count,
                        "qty": buy_count % 5 + 1,
                        "type": "limit",
                    }
                )
                buy_count += 1
        return {"orders": orders}

    orders = []
    for _ in range(200_000):
        side = "buy" if rng.integer(0, 1) == 0 else "sell"
        market = rng.integer(0, 9) == 0
        orders.append(
            {
                "side": side,
                "price": 0 if market else rng.integer(500, 1_500),
                "qty": rng.integer(1, 20),
                "type": "market" if market else "limit",
            }
        )
    return {"orders": orders}


def build_44(name: str, rng: Rng) -> dict[str, Any]:
    if name == "09_large_random":
        return {"s": rng.text(PROTEIN, 1_800), "t": rng.text(PROTEIN, 1_700)}
    source = list(rng.text(PROTEIN, 2_000))
    target = source.copy()
    for i in range(0, len(target), 50):
        target[i] = PROTEIN[(PROTEIN.index(target[i]) + 1) % len(PROTEIN)]
    return {"s": "".join(source[20:1_980]), "t": "".join(target)}


def build_45(name: str, rng: Rng) -> dict[str, Any]:
    k = 20 if name == "09_large_path" else 24
    alphabet = DNA if name == "09_large_path" else "AAACGT"
    genome = rng.text(alphabet, 200_000 + k - 1)
    kmers = [genome[i : i + k] for i in range(200_000)]
    return {"k": k, "kmers": kmers}


def build_46(name: str, rng: Rng) -> dict[str, Any]:
    if name == "46_large_many":
        length = 16
        genome = rng.text(DNA, 1_000_000)
        guides = [rng.text(DNA, length) for _ in range(2_000)]
        return {"d": 2, "len": length, "genome": genome, "guides": guides}
    guide = "CAAA" * 5
    return {
        "d": 3,
        "len": 20,
        "genome": "A" * 1_000_000,
        "guides": [guide for _ in range(2_000)],
    }


def build_47(name: str, rng: Rng) -> dict[str, Any]:
    if name == "10_large_random":
        return {"rna": rng.text(RNA, 380), "min_loop": 3, "allow_wobble": True}
    return {"rna": rng.text(RNA, 400), "min_loop": 0, "allow_wobble": False}


def build_48(name: str, rng: Rng) -> dict[str, Any]:
    length = 50 if name == "10_large_chain" else 80
    step = 20 if name == "10_large_chain" else 35
    genome = rng.text(DNA, step * 19_999 + length)
    reads = [genome[i * step : i * step + length] for i in range(20_000)]
    rng.shuffle(reads)
    return {"reads": reads}


def build_49(name: str, rng: Rng) -> dict[str, Any]:
    del rng
    if name == "09_large_three_regions":
        return {
            "sequence": "ACG" * 9 + "A",
            "start": [0, -3, -3],
            "transition": [[0, -2, -2], [-2, 0, -2], [-2, -2, 0]],
            "emission": [[10, -10, -10, -10], [-10, 10, -10, -10], [-10, -10, 10, -10]],
        }
    return {
        "sequence": "TGCA" * 6,
        "start": [-4, -4, -4, 0],
        "transition": [
            [1, -3, -3, -3],
            [-3, 1, -3, -3],
            [-3, -3, 1, -3],
            [-3, -3, -3, 1],
        ],
        "emission": [
            [12, -12, -12, -12],
            [-12, 12, -12, -12],
            [-12, -12, 12, -12],
            [-12, -12, -12, 12],
        ],
    }


def build_50(name: str, rng: Rng) -> dict[str, Any]:
    del rng
    parent = [-1] + [(i - 1) // 2 for i in range(1, 31)]
    if name == "09_large_balanced":
        sequences = [None] * 15 + list("ACGT" * 4)
        prior = [0.25, 0.25, 0.25, 0.25]
        diagonal = 0.94
        off_diagonal = 0.02
    else:
        sequences = [None] * 15 + ["AC", "CA", "GT", "TG"] * 4
        prior = [0.4, 0.3, 0.2, 0.1]
        diagonal = 0.85
        off_diagonal = 0.05
    transition = [
        [diagonal if i == j else off_diagonal for j in range(4)]
        for i in range(4)
    ]
    return {
        "parent": parent,
        "sequences": sequences,
        "prior": prior,
        "transition": transition,
    }


def build_51(name: str, rng: Rng) -> dict[str, Any]:
    del rng
    if name == "09_large_clock_jump":
        commands = [
            ["schedule", 10, 10_000_000_000],
            ["schedule", 20, 2],
            ["schedule", 30, 9_999_999_999],
            ["advance", 10_000_000_000],
        ]
    else:
        commands = [
            ["schedule", 1, 20_000_000_000],
            ["schedule", 2, 20],
            ["schedule", 1, 15_000_000_000],
            ["cancel", 2],
            ["schedule", 3, 14_999_999_999],
            ["advance", 15_000_000_000],
        ]
    return {"commands": commands}


def build_52(name: str, rng: Rng) -> dict[str, Any]:
    size = 12 if name == "09_large_twelve" else 13
    low = 1 if name == "09_large_twelve" else -3
    return {
        "costs": [[rng.integer(low, 100) for _ in range(size)] for _ in range(size)]
    }


def build_53(name: str, rng: Rng) -> dict[str, Any]:
    del rng
    blocks = list(range(1, 150_001))
    b = [blocks] if name == "09_large_same" else [[block] for block in blocks]
    return {"a": [blocks], "b": b}


def cyclic_spectrum(peptide: list[int]) -> list[int]:
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


def build_54(name: str, rng: Rng) -> dict[str, Any]:
    del rng
    if name == "09_large_six_masses":
        return {"masses": [57, 71, 87, 97, 99, 101], "spectrum": [0, 1_500]}
    peptide = [103, 57, 71, 99, 87, 101, 97, 57, 103, 71, 87]
    return {
        "masses": [57, 71, 87, 97, 99, 101, 103],
        "spectrum": cyclic_spectrum(peptide),
    }


def operation(kind: str, u: int, v: int) -> dict[str, Any]:
    return {"type": kind, "u": u, "v": v}


def build_55(name: str, rng: Rng) -> dict[str, Any]:
    del rng
    n = 40_000
    if name == "09_large_path":
        operations = [operation("add", i, i + 1) for i in range(n - 1)]
        operations.extend(operation("ask", 0, n - 1) for _ in range(n))
    else:
        operations = [operation("add", 0, i) for i in range(1, n)]
        operations.extend(operation("ask", 1, n - 1) for _ in range(n))
    return {"n": n, "operations": operations}


def build_56(name: str, rng: Rng) -> dict[str, Any]:
    del rng
    n = 150_000
    if name == "09_large_dense":
        horizontal = [[0, n, y] for y in range(n)]
        vertical = [[x, 0, n - 1] for x in range(n)]
    else:
        horizontal = [[3 * i, 3 * i + 1, i] for i in range(n)]
        vertical = [[3 * i + 2, 0, n - 1] for i in range(n)]
    return {"horizontal": horizontal, "vertical": vertical}


def event(event_id: int, process: int, clock: list[int]) -> dict[str, Any]:
    return {"id": event_id, "process": process, "clock": clock}


def build_57(name: str, rng: Rng) -> dict[str, Any]:
    processes = 4
    events = []
    if name == "09_large_independent":
        per_process = 30_000
        for process in range(processes):
            for sequence in range(1, per_process + 1):
                clock = [0] * processes
                clock[process] = sequence
                events.append(event(process * per_process + sequence, process, clock))
    else:
        counts = [0] * processes
        for i in range(80_000):
            process = i % processes
            counts[process] += 1
            events.append(event(i + 1, process, counts.copy()))
    rng.shuffle(events)
    return {"processes": processes, "events": events}


def build_58(name: str, rng: Rng) -> dict[str, Any]:
    n = 400_000
    if name == "09_large_percentile_ranks":
        # Wide value range, so almost every fill is distinct and the requested
        # ranks reach from both tails into the middle of the session.
        slippage = [rng.integer(-1_000_000_000, 1_000_000_000) for _ in range(n)]
        ks = [1, 2, 500, 40_000, 200_000, n - 1, n]
    else:
        # Eight tick values, 50_000 fills each, laid out non-decreasing: every
        # requested rank falls inside a 50_000-fill run of equal slippage, and
        # consecutive ranks straddle a run boundary.
        run = n // 8
        slippage = [value - 4 for value in range(8) for _ in range(run)]
        ks = [1, 50_000, 50_001, 200_000, 200_001, n]
    return {"n": n, "slippage": slippage, "ks": ks}


def build_59(name: str, rng: Rng) -> dict[str, Any]:
    n = 250_000
    prices: list[int] = []
    if name == "09_large_rising_ramp":
        # Every session settles above the one before it, all values distinct, so
        # no day of the series is undercut until the closing session prints
        # below the whole ramp.
        price = 0
        for _ in range(n - 1):
            price += rng.integer(1, 4_000)
            prices.append(price)
    else:
        # 250 plateaus of 1_000 equal settlements that never step down: an
        # undercut needs a strictly lower price, and only the closing session
        # has one, so equal neighbours must not be mistaken for undercuts.
        price = 0
        while len(prices) < n - 1:
            prices.extend([price] * min(1_000, n - 1 - len(prices)))
            price += rng.integer(0, 40)
    prices.append(-1)
    return {"n": n, "prices": prices}


def build_60(name: str, rng: Rng) -> dict[str, Any]:
    if name == "09_large_forked_chains":
        # Root with two 99_999-venue lines. Every pair takes one venue from the
        # deep quarter of each line, so the only venue on both routes is the
        # root and both routes run their full length.
        arm = 99_999
        n = 2 * arm + 1
        parent = [-1] * n
        for venue in range(1, n):
            parent[venue] = venue - 1
        parent[arm + 1] = 0
        deep = arm * 3 // 4
        queries = [
            [rng.integer(deep, arm), rng.integer(arm + deep, n - 1)] for _ in range(150)
        ]
        return {"n": n, "parent": parent, "queries": queries}

    # A 1_000-venue spine, then 25 branches of 7_960 hanging off its tail, with
    # every venue number shuffled so a parent's number says nothing about its
    # child's. Pairs come from the deep fifth of two different branches, so both
    # routes run far past the shared venue at the end of the spine.
    spine = 1_000
    branches = 25
    length = 7_960
    n = spine + branches * length
    parent = [-1] * n
    for venue in range(1, spine):
        parent[venue] = venue - 1
    for branch in range(branches):
        base = spine + branch * length
        parent[base] = spine - 1
        for step in range(1, length):
            parent[base + step] = base + step - 1
    label = list(range(n))
    rng.shuffle(label)
    shuffled = [-1] * n
    for venue in range(n):
        shuffled[label[venue]] = -1 if parent[venue] < 0 else label[parent[venue]]
    deep = length * 4 // 5
    queries = []
    for _ in range(1_800):
        first = rng.integer(0, branches - 1)
        second = (first + rng.integer(1, branches - 1)) % branches
        queries.append(
            [
                label[spine + first * length + rng.integer(deep, length - 1)],
                label[spine + second * length + rng.integer(deep, length - 1)],
            ]
        )
    return {"n": n, "parent": shuffled, "queries": queries}


def build_61(name: str, rng: Rng) -> dict[str, Any]:
    if name == "09_large_cycle_chain":
        # 66_666 three-venue loops strung out in one line, neighbouring loops
        # joined by a single link. Half the network sits behind every joining
        # link, and the line is 199_998 venues from end to end.
        blocks = 66_666
        links = []
        for block in range(blocks):
            base = 3 * block
            links.append([base, base + 1])
            links.append([base + 1, base + 2])
            links.append([base + 2, base])
            if block:
                links.append([base - 1, base])
        return {"n": 3 * blocks, "links": links}

    # A 120_000-venue ring with 40_000 extra links thrown across it, 50_000 more
    # venues hung off the result in trees, 5_000 of those hanging links doubled,
    # and a detached 30_000-venue line. Venue numbers and link order are both
    # shuffled, so neither says anything about the shape.
    ring = 120_000
    hanging = 50_000
    line = 30_000
    n = ring + hanging + line
    links = [[venue, venue + 1] for venue in range(ring - 1)]
    links.append([ring - 1, 0])
    for _ in range(40_000):
        venue = rng.integer(0, ring - 1)
        links.append([venue, (venue + rng.integer(1, ring - 1)) % ring])
    hung = []
    for step in range(hanging):
        child = ring + step
        hung.append([rng.integer(0, child - 1), child])
    links.extend(hung)
    order = list(range(hanging))
    rng.shuffle(order)
    links.extend(hung[pick] for pick in order[:5_000])
    base = ring + hanging
    links.extend([base + step, base + step + 1] for step in range(line - 1))
    label = list(range(n))
    rng.shuffle(label)
    links = [[label[u], label[v]] for u, v in links]
    rng.shuffle(links)
    return {"n": n, "links": links}


def build_62(name: str, rng: Rng) -> dict[str, Any]:
    n = 38
    if name == "09_large_signed_spread":
        # 38 positions drawn across the whole signed range and a target drawn
        # independently of them. No two positions share a magnitude, so the
        # baskets have essentially 2**38 distinct totals and nothing about the
        # book narrows where the closest one sits.
        exposures = [rng.integer(-(10**12), 10**12) for _ in range(n)]
        target = rng.integer(-(10**12), 10**12)
    else:
        # 38 positions of one sign, all even, and an odd target at half the
        # book's total: totals crowd the target from both sides, every position
        # is in play, and no basket can land on it exactly. The magnitudes stay
        # under 4 * 10**11, which keeps the target inside its own limit whatever
        # the draw.
        exposures = [2 * rng.integer(5 * 10**10, 2 * 10**11) for _ in range(n)]
        target = sum(exposures) // 2 | 1
    return {"n": n, "target": target, "exposures": exposures}


def build_63(name: str, rng: Rng) -> dict[str, Any]:
    n = 1_000_000
    quantities: list[int] = []
    if name == "09_large_rising_wall":
        # Every level rests strictly more than the one before it and all million
        # quantities are distinct. A sweep sized to any level's own quantity is
        # available at every later level, so the run outward from a level reaches
        # the far end of the book, and the shape says nothing about where the
        # largest block sits.
        quantity = 0
        for _ in range(n):
            quantity += rng.integer(1, 1_000)
            quantities.append(quantity)
    else:
        # 1000 plateaus of 1000 equal quantities, laid out non-increasing, with
        # every tenth step down set to 0 so that a hundred pairs of plateaus join
        # into one 2000-level run of exactly equal quantities. No level rests
        # more than the one before it, so the run from a level reaches back to
        # the top of the book, and equal neighbours must not cut a run short.
        steps = [
            0 if i % 10 == 4 else rng.integer(1, 5_000) for i in range(n // 1_000)
        ]
        quantity = sum(steps)
        for step in steps:
            quantities.extend([quantity] * 1_000)
            quantity -= step
    return {"n": n, "quantities": quantities}


def build_64(name: str, rng: Rng) -> dict[str, Any]:
    n = 500_000
    left = [-1] * n
    right = [-1] * n
    if name == "09_large_skewed_chain":
        # One 500000-desk line, each desk reporting to the one above it and the
        # side alternating so neither child slot is the only one used. Nothing is
        # ever a meeting point of two arms, so the whole answer comes out of the
        # value handed upward, and both the depth and the walk from any desk run
        # the length of the hierarchy. Contributions are drawn across the whole
        # allowed range, so the winning run is a window somewhere in the middle
        # and its total is far past a signed 32-bit integer.
        pnl = [rng.integer(-(10**9), 10**9) for _ in range(n)]
        chain = list(range(n))
        rng.shuffle(chain)
        for step in range(n - 1):
            if step % 2 == 0:
                left[chain[step]] = chain[step + 1]
            else:
                right[chain[step]] = chain[step + 1]
        return {"n": n, "root": chain[0], "pnl": pnl, "left": left, "right": right}

    # A 250000-desk spine with one leaf desk hanging off every spine desk, so
    # every spine desk is a meeting point of two arms and half the hierarchy is
    # leaves. Spine contributions are drawn across the whole allowed range and
    # leaf contributions too, so about half the leaves are worth taking at the
    # turn and the other half must be dropped. Desk numbers are shuffled, so a
    # parent's number says nothing about its children's.
    spine = n // 2
    pnl = [rng.integer(-(10**9), 10**9) for _ in range(n)]
    label = list(range(n))
    rng.shuffle(label)
    for step in range(spine):
        left[label[step]] = label[spine + step]
        if step + 1 < spine:
            right[label[step]] = label[step + 1]
    return {"n": n, "root": label[0], "pnl": pnl, "left": left, "right": right}


def build_65(name: str, rng: Rng) -> dict[str, Any]:
    if name == "09_large_layered_feeds":
        # Four layers of 7500 strategies. The bottom layer is pure cost, drawn
        # small enough that a shared prerequisite is worth paying for once but
        # not twice; every strategy above it names three prerequisites in the
        # layer below, picked independently, so prerequisites are shared by about
        # three dependants each and no strategy stands alone. Contributions above
        # the bottom layer span the whole allowed range, so roughly half of them
        # are losses that only a dependant can justify. No prerequisite ever
        # points upward or sideways: the whole recipe is one shallow acyclic
        # graph, and its answer keeps a little under half of what the profitable
        # strategies would be worth if prerequisites were free.
        layers = 4
        per_layer = 7_500
        n = layers * per_layer
        pnl = [0] * n
        requires = []
        for layer in range(layers):
            for slot in range(per_layer):
                strategy = layer * per_layer + slot
                if layer == 0:
                    pnl[strategy] = -rng.integer(10**6, 10**8)
                    continue
                pnl[strategy] = rng.integer(-(10**9), 10**9)
                below = (layer - 1) * per_layer
                for _ in range(3):
                    requires.append([strategy, below + rng.integer(0, per_layer - 1)])
        return {"n": n, "pnl": pnl, "requires": requires}

    # 4000 clusters of five strategies, each cluster wired as a directed cycle so
    # its five members are all-or-nothing however their contributions fall. The
    # clusters sit in four ranks of 1000; every cluster outside the first rank
    # names two prerequisites in the rank below, so a cluster drags whole other
    # clusters in with it and the closure of one strategy can be far larger than
    # its own cluster. Contributions span the whole allowed range, so a cluster's
    # own five may total either way and the decision is never local.
    size = 5
    clusters = 4_000
    ranks = 4
    per_rank = clusters // ranks
    n = clusters * size
    pnl = [rng.integer(-(10**9), 10**9) for _ in range(n)]
    requires = []
    for cluster in range(clusters):
        base = cluster * size
        for member in range(size):
            requires.append([base + member, base + (member + 1) % size])
        rank = cluster // per_rank
        if rank == 0:
            continue
        for _ in range(2):
            other = ((rank - 1) * per_rank + rng.integer(0, per_rank - 1)) * size
            requires.append(
                [base + rng.integer(0, size - 1), other + rng.integer(0, size - 1)]
            )
    return {"n": n, "pnl": pnl, "requires": requires}


BUILDERS: dict[str, Callable[[str, Rng], dict[str, Any]]] = {
    "01-easy-max-subarray": build_01,
    "02-easy-mod-exp": build_02,
    "03-easy-max-drawdown": build_03,
    "04-medium-edge-costs": build_04,
    "05-medium-price-streak": build_05,
    "06-medium-edit-distance": build_06,
    "07-medium-coin-change": build_07,
    "08-medium-interval-scheduling": build_08,
    "09-medium-count-inversions": build_09,
    "10-medium-route-costs": build_10,
    "11-medium-friend-groups": build_11,
    "12-medium-textbook-split": build_12,
    "13-medium-sliding-window-max": build_13,
    "14-medium-count-primes": build_14,
    "15-medium-huge-fibonacci": build_15,
    "16-medium-string-search": build_16,
    "17-medium-knapsack": build_17,
    "18-medium-task-ordering": build_18,
    "19-medium-mst": build_19,
    "20-medium-lcs": build_20,
    "23-medium-search-suggestions": build_23,
    "24-medium-lru-cache": build_24,
    "25-medium-running-median": build_25,
    "26-medium-dynamic-prefix-sums": build_26,
    "27-medium-weighted-job-scheduling": build_27,
    "28-medium-news-feed-merge": build_28,
    "35-hard-dynamic-range-sums": build_35,
    "36-hard-matrix-chain": build_36,
    "37-hard-prime-pair-sets": build_37,
    "38-hard-distinct-substrings": build_38,
    "39-hard-max-flow": build_39,
    "41-hard-ordered-set-queries": build_41,
    "42-hard-fragmented-string-queries": build_42,
    "43-hard-order-book": build_43,
    "44-hard-affine-align": build_44,
    "45-hard-kmer-assembly": build_45,
    "46-hard-crispr-offtarget": build_46,
    "47-hard-rna-max-pairs": build_47,
    "48-hard-shortest-superstring": build_48,
    "49-hard-gene-region-decoder": build_49,
    "50-hard-tree-sequence-likelihood": build_50,
    "51-hard-deadline-scheduler": build_51,
    "52-hard-service-pairing": build_52,
    "53-hard-circular-genome-distance": build_53,
    "54-hard-spectrum-peptide-recovery": build_54,
    "55-hard-changing-network-queries": build_55,
    "56-hard-orthogonal-segment-crossings": build_56,
    "57-hard-causal-event-replay": build_57,
    "58-medium-kth-worst-fill": build_58,
    "59-medium-price-undercut": build_59,
    "60-medium-venue-ancestor": build_60,
    "61-hard-critical-venue-links": build_61,
    "62-hard-neutral-basket": build_62,
    "63-hard-liquidity-wall": build_63,
    "64-medium-signal-path": build_64,
    "65-hard-strategy-portfolio": build_65,
}

NAMES = {
    "01-easy-max-subarray": ("09_large_random", "10_large_negative"),
    "02-easy-mod-exp": ("09_large_exp", "10_large_base"),
    "03-easy-max-drawdown": ("09_large_decline", "10_large_random"),
    "04-medium-edge-costs": ("09_large_path", "10_large_star", "11_large_caterpillar"),
    "05-medium-price-streak": ("09_large_increasing", "10_large_random"),
    "06-medium-edit-distance": ("09_large_random", "10_large_binary"),
    "07-medium-coin-change": ("09_large_amount", "10_large_sparse"),
    "08-medium-interval-scheduling": ("09_large_random", "10_large_chain"),
    "09-medium-count-inversions": ("09_large_reversed", "10_large_random"),
    "10-medium-route-costs": ("09_large_sparse", "10_large_path"),
    "11-medium-friend-groups": ("09_large_random", "10_large_chain"),
    "12-medium-textbook-split": ("09_large_random", "10_large_wide"),
    "13-medium-sliding-window-max": ("09_large_random", "10_large_decreasing"),
    "14-medium-count-primes": ("09_large_ten_million", "10_large_hundred_million"),
    "15-medium-huge-fibonacci": ("09_large_n", "10_large_n2"),
    "16-medium-string-search": ("09_large_allmatch", "10_large_nearmiss"),
    "17-medium-knapsack": ("09_large_random", "10_large_small_weights"),
    "18-medium-task-ordering": ("09_large_dag", "10_large_path"),
    "19-medium-mst": ("09_large_random", "10_large_chain"),
    "20-medium-lcs": ("09_large_dna", "10_large_binary"),
    "23-medium-search-suggestions": ("09_large_dense", "10_large_wide"),
    "24-medium-lru-cache": ("09_large_mixed", "10_large_thrash"),
    "25-medium-running-median": ("09_large_random", "10_large_sorted"),
    "26-medium-dynamic-prefix-sums": ("09_large_mixed", "10_large_queries"),
    "27-medium-weighted-job-scheduling": ("09_large_random", "10_large_touching"),
    "28-medium-news-feed-merge": ("09_large_many", "10_large_skew"),
    "35-hard-dynamic-range-sums": ("09_large_mixed", "10_large_queries"),
    "36-hard-matrix-chain": ("09_large_random", "10_large_big"),
    "37-hard-prime-pair-sets": ("09_large_full", "10_large_extended"),
    "38-hard-distinct-substrings": ("09_large_random", "10_large_binary"),
    "39-hard-max-flow": ("09_large_random", "10_large_parallel"),
    "41-hard-ordered-set-queries": (
        "09_large_search",
        "10_large_range",
        "12_large_full_range",
    ),
    "42-hard-fragmented-string-queries": ("09_large_windows", "10_large_wide"),
    "43-hard-order-book": ("09_large_deep_book", "10_large_churn"),
    "44-hard-affine-align": ("09_large_random", "10_large_similar"),
    "45-hard-kmer-assembly": ("09_large_path", "10_large_skewed"),
    "46-hard-crispr-offtarget": ("46_large_many", "46_large_repeat"),
    "47-hard-rna-max-pairs": ("10_large_random", "11_large_hairpin"),
    "48-hard-shortest-superstring": ("10_large_chain", "11_large_dense"),
    "49-hard-gene-region-decoder": ("09_large_three_regions", "10_large_four_regions"),
    "50-hard-tree-sequence-likelihood": ("09_large_balanced", "10_large_balanced_sites"),
    "51-hard-deadline-scheduler": ("09_large_clock_jump", "10_large_replacements"),
    "52-hard-service-pairing": ("09_large_twelve", "10_large_thirteen"),
    "53-hard-circular-genome-distance": ("09_large_same", "10_large_singletons"),
    "54-hard-spectrum-peptide-recovery": ("09_large_six_masses", "10_large_seven_masses"),
    "55-hard-changing-network-queries": ("09_large_path", "10_large_star"),
    "56-hard-orthogonal-segment-crossings": ("09_large_dense", "10_large_sparse"),
    "57-hard-causal-event-replay": ("09_large_independent", "10_large_chain"),
    "58-medium-kth-worst-fill": (
        "09_large_percentile_ranks",
        "10_large_duplicate_plateaus",
    ),
    "59-medium-price-undercut": ("09_large_rising_ramp", "10_large_equal_plateaus"),
    "60-medium-venue-ancestor": ("09_large_forked_chains", "10_large_shuffled_fan"),
    "61-hard-critical-venue-links": (
        "09_large_cycle_chain",
        "10_large_ring_and_hangers",
    ),
    "62-hard-neutral-basket": (
        "09_large_signed_spread",
        "10_large_same_sign_split",
    ),
    "63-hard-liquidity-wall": (
        "09_large_rising_wall",
        "10_large_draining_plateaus",
    ),
    "64-medium-signal-path": (
        "09_large_skewed_chain",
        "10_large_caterpillar_desks",
    ),
    "65-hard-strategy-portfolio": (
        "09_large_layered_feeds",
        "10_large_cyclic_clusters",
    ),
}

REPEATS = {
    ("18-medium-task-ordering", "09_large_dag"): 2,
    ("18-medium-task-ordering", "10_large_path"): 2,
    ("35-hard-dynamic-range-sums", "09_large_mixed"): 2,
    ("35-hard-dynamic-range-sums", "10_large_queries"): 2,
}


def get_cases(challenge: str) -> list[Case]:
    try:
        names = NAMES[challenge]
    except KeyError as exc:
        raise ValueError(f"Unknown I/O challenge: {challenge}") from exc
    number = int(challenge[:2])
    return [
        Case(
            challenge=challenge,
            name=name,
            seed=number * 100 + i,
            repeats=REPEATS.get((challenge, name), 1),
        )
        for i, name in enumerate(names, start=1)
    ]


def build_case(case: Case) -> dict[str, Any]:
    return BUILDERS[case.challenge](case.name, Rng(case.seed))


def write_case(case: Case, output: TextIO | None) -> str:
    digest = hashlib.sha256()

    class Writer:
        def write(self, text: str) -> int:
            if output is not None:
                output.write(text)
            digest.update(text.encode())
            return len(text)

    writer = Writer()
    json.dump(build_case(case), writer, separators=(",", ":"))
    writer.write("\n")
    return digest.hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("challenge", nargs="?", choices=sorted(NAMES))
    parser.add_argument("case", nargs="?")
    parser.add_argument("output", nargs="?", type=Path)
    return parser.parse_args()


def check_cases() -> None:
    hashes = {}
    for challenge in sorted(NAMES):
        hashes[challenge] = {
            case.name: {
                "seed": case.seed,
                "repeats": case.repeats,
                "sha256": write_case(case, None),
            }
            for case in get_cases(challenge)
        }
    manifest = json.dumps(hashes, indent=2, sort_keys=True) + "\n"
    digest = hashlib.sha256(manifest.encode()).hexdigest()
    if digest != EXPECTED_DIGEST:
        raise SystemExit(
            f"Generated large cases changed: {digest} != {EXPECTED_DIGEST}"
        )
    print(f"{sum(map(len, NAMES.values()))} generated large cases are reproducible")


def main() -> None:
    args = parse_args()
    if args.check:
        check_cases()
        return
    if args.challenge is None:
        raise SystemExit("Challenge is required unless --check is used")
    cases = get_cases(args.challenge)
    if args.case is None:
        for case in cases:
            print(f"{case.name} seed={case.seed} repeats={case.repeats}")
        return
    case = next((item for item in cases if item.name == args.case), None)
    if case is None:
        raise SystemExit(f"Unknown large case for {args.challenge}: {args.case}")
    if args.output is None:
        raise SystemExit("Output path is required when a case is selected")
    with args.output.open("w", encoding="utf-8") as output:
        digest = write_case(case, output)
    print(
        f"{case.name} seed={case.seed} repeats={case.repeats} sha256={digest}"
    )


if __name__ == "__main__":
    main()

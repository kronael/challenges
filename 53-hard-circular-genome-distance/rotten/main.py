import json
import sys


def colored_edges(genome):
    edges = []
    for chromosome in genome:
        nodes = []
        for block in chromosome:
            value = abs(block)
            if block > 0:
                nodes.extend((2 * value - 1, 2 * value))
            else:
                nodes.extend((2 * value, 2 * value - 1))
        for i in range(1, len(nodes), 2):
            edges.append((nodes[i], nodes[(i + 1) % len(nodes)]))
    return edges


def find_partner(edges, node):
    for a, b in edges:
        if a == node:
            return b
        if b == node:
            return a
    raise ValueError("missing extremity")


def solve(a, b):
    red = colored_edges(a)
    blue = colored_edges(b)
    seen = set()
    cycles = 0
    # Naive: find every alternating partner by rescanning all n edges. Correct,
    # but O(n²) repeated lookup TIMEOUTs on the large genomes.
    for edge in red:
        for start in edge:
            if start in seen:
                continue
            cycles += 1
            node = start
            while node not in seen:
                seen.add(node)
                node = find_partner(red, node)
                seen.add(node)
                node = find_partner(blue, node)
    return len(red) - cycles


def main():
    obj = json.load(sys.stdin)
    print(solve(obj["a"], obj["b"]))


if __name__ == "__main__":
    main()

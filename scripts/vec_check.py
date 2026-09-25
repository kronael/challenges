"""Report whether a function compiled to packed SIMD instructions.

A vec challenge is graded on the shape of the emitted code, not on wall time.
Its golden reference must vectorize and its rotten control must not, and both
have the same complexity, so a timing gate cannot separate them.

Builds for x86-64-v3, the AVX2 baseline, rather than the host CPU, so a verdict
is reproducible on any machine that can build the repository. Go names that
target GOAMD64=v3, and builds with GOEXPERIMENT=simd so that `simd/archsimd`
can be imported.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

TARGET = "x86-64-v3"
GO_ENV = {"GOAMD64": "v3", "GOEXPERIMENT": "simd"}

# Packed arithmetic, comparison, shuffle, and mask extraction. Scalar forms end
# in ss/sd and are absent on purpose: they are what a failed vectorization
# leaves behind. Logical ops are absent too, because vxorps is the
# register-zeroing idiom and appears just as often in scalar code.
PACKED = re.compile(
    r"^\s*v?("
    r"(add|sub|mul|div|max|min|sqrt|rcp|rsqrt|cmp|blend|round|movmsk)p[sd]"
    r"|f(n?madd|n?msub)[0-9]*p[sd]"
    r"|p(add|sub|mull|mulh|maxs|maxu|mins|minu|cmpeq|cmpgt|shufb|shufd"
    r"|blendvb|ackus|ackss|unpck|sll|srl|sra|avg|sad|movmskb)[a-z]*"
    r"|perm[a-z0-9]*|broadcast[a-z0-9]*|gather[a-z0-9]*"
    r")\b",
    re.IGNORECASE,
)
SCALAR = re.compile(r"^\s*v?(add|sub|mul|div|max|min|sqrt|cmp|f?n?madd[0-9]*)s[sd]\b", re.IGNORECASE)

LABEL = re.compile(r"^\s*(\.[\w.$]+):")
# A conditional branch to a label. Plain jmp is excluded: it also jumps
# backwards, to rejoin a tail the compiler hoisted out of line, and that is not
# a loop.
BRANCH = re.compile(r"^\s*j(?!mpq?\b)\w+\s+(\.[\w.$]+)\s*$")

# Go's -S output heads each function with `main.NAME STEXT` and prints one
# instruction per line after its hex and decimal offsets and its source
# position. The hex dump and relocations that follow a function have no source
# position, so they never match.
GO_SYMBOL = re.compile(r"^main\.(\S+) STEXT\b")
GO_INSTRUCTION = re.compile(r"^\t0x[0-9a-f]+ (\d+) \(.*?\)\t(\w+)\t?(.*)$")


def go_listing(compiled: str) -> str:
    """Go's -S output in the shape of a GNU listing, so that the parser which
    reads C and Rust assembly reads Go's too.

    Go names a branch target by its decimal offset rather than by a label. This
    puts `NAME:` and `.size NAME` around each function of package main, a
    `.L<offset>:` label before every branch target, and points each branch at
    that label.
    """
    functions: list[tuple[str, list[tuple[int, str, str]]]] = []
    current: list[tuple[int, str, str]] | None = None
    for line in compiled.splitlines():
        if line and not line[0].isspace():
            symbol = GO_SYMBOL.match(line)
            current = [] if symbol else None
            if symbol:
                functions.append((symbol.group(1), current))
            continue
        instruction = GO_INSTRUCTION.match(line)
        if instruction and current is not None:
            offset, mnemonic, operands = instruction.groups()
            current.append((int(offset), mnemonic.lower(), operands))

    out = []
    for name, instructions in functions:
        targets = {int(operands) for _, mnemonic, operands in instructions
                   if mnemonic.startswith("j") and operands.isdigit()}
        out.append(f"{name}:")
        for offset, mnemonic, operands in instructions:
            if offset in targets:
                out.append(f".L{offset}:")
                targets.discard(offset)
            if mnemonic.startswith("j") and operands.isdigit():
                operands = f".L{operands}"
            out.append(f"\t{mnemonic}\t{operands}")
        out.append(f"\t.size\t{name}, .-{name}")
    return "\n".join(out) + "\n"


def assembly(workdir: Path, lang: str) -> str:
    if lang == "go":
        done = subprocess.run(
            ["go", "build", "-gcflags=-S", "-o", os.devnull, "."],
            cwd=workdir, capture_output=True, text=True, env={**os.environ, **GO_ENV},
        )
        if done.returncode != 0:
            sys.exit(f"vec_check: go build failed\n{done.stderr}")
        return go_listing(done.stderr)

    if lang == "c":
        sources = sorted(p.name for p in workdir.glob("*.c"))
        if not sources:
            sys.exit(f"vec_check: no .c sources in {workdir}")
        done = subprocess.run(
            ["cc", "-std=c11", "-O3", f"-march={TARGET}", "-S", "-o", "-", *sources],
            cwd=workdir, capture_output=True, text=True,
        )
        if done.returncode != 0:
            sys.exit(f"vec_check: compile failed\n{done.stderr}")
        return done.stdout

    done = subprocess.run(
        ["cargo", "rustc", "--release", "--lib", "--quiet", "--",
         "--emit", "asm", "-C", f"target-cpu={TARGET}"],
        cwd=workdir, capture_output=True, text=True,
    )
    if done.returncode != 0:
        sys.exit(f"vec_check: cargo failed\n{done.stderr}")
    emitted = sorted((workdir / "target/release/deps").glob("*.s"), key=lambda p: p.stat().st_mtime)
    if not emitted:
        sys.exit("vec_check: cargo emitted no assembly")
    return emitted[-1].read_text()


def body(asm: str, name: str) -> str | None:
    """The assembly between a symbol's label and its .size directive."""
    label = re.search(rf"^{re.escape(name)}:", asm, re.MULTILINE)
    if label is None:
        return None
    rest = asm[label.end():]
    end = re.search(rf"^\s*\.size\s+{re.escape(name)}\b", rest, re.MULTILINE)
    return rest[: end.start()] if end else rest


def loops(lines: list[str]) -> list[list[str]]:
    """Every loop body: a label, and a later conditional branch back to it."""
    labelled: dict[str, int] = {}
    found = []
    for index, line in enumerate(lines):
        label = LABEL.match(line)
        if label:
            labelled[label.group(1)] = index
        branch = BRANCH.match(line)
        if branch and branch.group(1) in labelled:
            found.append(lines[labelled[branch.group(1)] : index + 1])
    return found


def arithmetic(loop: list[str]) -> tuple[int, int]:
    """How many packed and how many scalar arithmetic instructions a loop runs."""
    return (
        sum(1 for line in loop if PACKED.match(line)),
        sum(1 for line in loop if SCALAR.match(line)),
    )


def verdict(lines: list[str]) -> tuple[str, list[tuple[int, int]]]:
    """A function is vectorized when one of its loops keeps ALL its arithmetic
    in vector lanes: packed instructions, and not one scalar instruction.

    Counting over the whole function cannot decide this. A correctly vectorized
    reduction emits MORE scalar instructions than the scalar version it beats,
    because its horizontal sum and its remainder tail are legitimately scalar.
    Only the loop bodies separate the two, and they separate them absolutely:
    the vectorized loop has no scalar arithmetic left in it at all, while a
    loop the compiler gave up on keeps its serial dependency in scalar
    registers however much packed work surrounds it.
    """
    shape = [arithmetic(loop) for loop in loops(lines)]
    vectorized = any(packed and not scalar for packed, scalar in shape)
    return "vectorized" if vectorized else "scalar", shape


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workdir", type=Path, default=Path.cwd())
    parser.add_argument("--lang", choices=("rust", "c", "go"), required=True)
    parser.add_argument("--function", action="append", required=True)
    parser.add_argument("--expect", choices=("vectorized", "scalar"), required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    asm = assembly(args.workdir.resolve(), args.lang)
    failed = False
    for name in args.function:
        lines = body(asm, name)
        if lines is None:
            print(f"  {name}: NOT FOUND — needs #[no_mangle] or external linkage")
            failed = True
            continue
        found, shape = verdict(lines.splitlines())
        ok = found == args.expect
        failed |= not ok
        loop_shapes = " ".join(f"{packed}p/{scalar}s" for packed, scalar in shape) or "no loops"
        print(f"  {name}: {loop_shapes} -> {found}"
              f"{'' if ok else '  EXPECTED ' + args.expect}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()

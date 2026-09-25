"""Grade whether a solve does its per-element work in packed SIMD lanes.

A vec challenge is graded on the instructions the compiler emitted, weighted by
how often they run. This runs the built binary on one input under ptrace, stops
at the entry of the graded function, and single-steps every instruction until
that call returns: its own code, every helper it calls, and every library
routine those call. Each instruction is classified from objdump's disassembly
of the running process.

The grade counts scalar work, of two kinds:

- scalar floating-point arithmetic, compares, and conversions; loads and stores
  that do not address the stack, through a general-purpose register of any
  width or through a vector register one element at a time; and moves of one
  lane out of a vector register into a general-purpose one, wherever they run;
- arithmetic, logic, compares, shifts, bit manipulation, and conditional sets
  and moves on general-purpose registers, except in vector iterations.

The instruction stream is cut into iterations at every backward jump, and an
iteration that loads several elements into a vector register in one instruction
is a vector iteration. Its general-purpose bookkeeping, loop control, bounds
checks, and mask arithmetic, is paid once per vector rather than once per
element, and is what separates C, Rust, and Go most; leaving it out lets one
budget mean the same thing in all three. Packed arithmetic, moves between
registers, stack accesses, string instructions such as rep movsb, and control
flow count on neither side.

The count is divided by the length of one array in the input, the challenge's
unit of work. A function is vectorized when it retires fewer than BUDGET
scalar instructions per unit and at least PACKED_FLOOR packed ones. Any scalar
pass over the input costs at least one per unit, a load or a floating-point
add, however many vector loops run beside it, while setup, a remainder tail,
and a horizontal sum cost a fraction of one. A loop the input never runs costs
nothing.

Before tracing, the solver's sources are checked for the ways to emit code the
compiler did not choose for x86-64-v3: inline or standalone assembly, pragmas
and attributes that change the target or the optimizer, Rust's
`#[target_feature]`, and build scripts and cgo that compile code outside the
graded build. While tracing, an AVX-512 instruction in the program's own code
is refused for the same reason.

Go's asynchronous preemption and collector are switched off, and Go's
runtime.morestack, where a goroutine's stack grows and where the scheduler
preempts it, runs untraced until it resumes the function that called it: all
three interrupt the traced thread with work that is not the solver's. A grade
that takes longer than TIMEOUT seconds fails, and the traced program dies with
the grader.
"""

from __future__ import annotations

import argparse
import ctypes
import enum
import json
import os
import re
import signal
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

BUDGET = 1.0
PACKED_FLOOR = 0.02
WINDOW = 256
LONGEST = 15
TIMEOUT = 60
MORESTACK = "runtime.morestack.abi0"
WORD = 2**64 - 1
REFUSED = 126

TRACEME = 0
PEEKTEXT = 1
POKETEXT = 4
CONT = 7
SINGLESTEP = 9
GETREGS = 12
SETREGS = 13
DETACH = 17
SET_PDEATHSIG = 1

libc = ctypes.CDLL(None, use_errno=True)
libc.ptrace.restype = ctypes.c_long
libc.ptrace.argtypes = (ctypes.c_long, ctypes.c_long, ctypes.c_void_p, ctypes.c_void_p)


class Regs(ctypes.Structure):
    _fields_ = [(name, ctypes.c_ulonglong) for name in (
        "r15 r14 r13 r12 rbp rbx r11 r10 r9 r8 rax rcx rdx rsi rdi orig_rax "
        "rip cs eflags rsp ss fs_base gs_base ds es fs gs").split()]


class Kind(enum.Enum):
    INTEGER = "integer"
    SCALAR = "scalar"
    PACKED = "packed"
    OTHER = "other"


@dataclass(frozen=True, slots=True)
class Insn:
    kind: Kind
    jump: bool
    vector_load: bool
    evex: bool


@dataclass
class Count:
    scalar: int = 0
    packed: int = 0
    returned: bool = False


PREFIXES = {"lock", "rep", "repz", "repe", "repnz", "repne", "notrack", "bnd",
            "data16", "addr32", "cs", "ds", "es", "fs", "gs", "ss"}
LEGACY_PREFIX_BYTES = {0x26, 0x2E, 0x36, 0x3E, 0x64, 0x65, 0x67}
VECTOR_REGISTER = re.compile(r"%[xyz]mm\d")
GPR_ARITHMETIC = re.compile(
    r"^(add|sub|adc|sbb|inc|dec|neg|not|and|andn|or|xor|imul|mul|div|idiv"
    r"|cmp|test|sal|sar|shl|shr|rol|ror|rcl|rcr|shld|shrd|sarx|shlx|shrx|rorx"
    r"|lea|bt|btc|btr|bts|bsf|bsr|popcnt|lzcnt|tzcnt|bextr|blsi|blsmsk|blsr"
    r"|bzhi|pdep|pext|mulx|adcx|adox|xadd|bswap|cbtw|cwtl|cltq|cwtd|cltd|cqto"
    r")[bwlq]?$|^(set|cmov)[a-z]+$|^cmpxchg"
)
X87_ARITHMETIC = re.compile(r"^fi?(add|sub|subr|mul|div|divr|com|ucom|sqrt|abs|chs)")
VECTOR_MOVE = re.compile(
    r"^v?(mov(?!msk)|maskmov|pmaskmov|lddqu|broadcast|pbroadcast|insert|extract"
    r"|pinsr|pextr|zero)"
)
SCALAR_FLOAT = re.compile(
    r"^v?((add|sub|mul|div|min|max|sqrt|rcp|rsqrt|round|cmp[a-z_]*|u?comi"
    r"|f(n?madd|n?msub)\d*|getexp|getmant|scalef|rndscale|range|reduce"
    r"|fixupimm)s[sdh]"
    r"|cvt(t?s[sdh]2u?si|u?si2s[sdh][lq]?|s[sdh]2s[sdh]))$"
)
ELEMENT_ACCESS = re.compile(
    r"^v?(movd|movq|movss|movsd|movsh|movhp[sd]|movlp[sd]|pinsr[bwdq]|pextr[bwdq]"
    r"|extractps|pbroadcast[bwdq]|broadcasts[sdh]|movddup)$"
)
GENERAL_REGISTER = re.compile(r"%(r[a-z0-9]+|e[a-z]{2}|[a-d][lhx]|[sd]il?|[sb]pl?)$")
STACK = re.compile(r"\(%[re](sp|bp)\b")
NO_ACCESS = re.compile(r"^(lea|nop|prefetch|j|call|endbr|clflush|clwb)")
STRING = re.compile(r"^(movs|stos|lods|cmps|scas)[bwlq]?$")

C_BANNED = [
    (re.compile(r"\b(asm|__asm__|__asm)\b"), "inline assembly"),
    (re.compile(r"^\s*#\s*pragma\b|\b_Pragma\s*\(", re.MULTILINE), "a #pragma"),
    (re.compile(r"\b_*(target|optimize|target_clones)_*\s*\("), "a target or optimize attribute"),
]
RUST_BANNED = [
    (re.compile(r"\b(asm|global_asm|naked_asm)!"), "inline assembly"),
    (re.compile(r"#!?\[\s*(unsafe\s*\(\s*)?(target_feature|naked)\b"), "#[target_feature] or #[naked]"),
]
GO_BANNED = [
    (re.compile(r'^\s*import\s*(\(\s*)?"C"', re.MULTILINE), "cgo"),
]
GO_OUTSIDE = {".s", ".S", ".syso", ".c", ".cc", ".cpp"}


def ptrace(request: int, pid: int, addr: int = 0, data: int = 0) -> int:
    ctypes.set_errno(0)
    result = libc.ptrace(request, pid, ctypes.c_void_p(addr), ctypes.c_void_p(data))
    error = ctypes.get_errno()
    if result == -1 and error:
        raise OSError(error, f"ptrace: {os.strerror(error)}")
    return result


def split_operands(operands: str) -> list[str]:
    parts = []
    depth = 0
    start = 0
    for index, char in enumerate(operands):
        depth += (char == "(") - (char == ")")
        if char == "," and depth == 0:
            parts.append(operands[start:index])
            start = index + 1
    parts.append(operands[start:])
    return [part.strip() for part in parts if part.strip()]


def decode(mnemonic: str, operands: str, first_byte: int) -> Insn:
    parts = split_operands(operands.partition("#")[0])
    vector = any(VECTOR_REGISTER.search(part) for part in parts)
    memory = (any("(" in part and not STACK.search(part) for part in parts)
              and not NO_ACCESS.match(mnemonic))
    extracts = bool(parts) and GENERAL_REGISTER.match(parts[-1]) is not None
    if STRING.match(mnemonic):
        kind = Kind.OTHER
    elif vector and VECTOR_MOVE.match(mnemonic):
        element = ELEMENT_ACCESS.match(mnemonic) and (memory or extracts)
        kind = Kind.SCALAR if element else Kind.OTHER
    elif vector:
        kind = Kind.SCALAR if SCALAR_FLOAT.match(mnemonic) else Kind.PACKED
    elif memory or X87_ARITHMETIC.match(mnemonic):
        kind = Kind.SCALAR
    elif GPR_ARITHMETIC.match(mnemonic):
        kind = Kind.INTEGER
    else:
        kind = Kind.OTHER
    loads = any("(" in part for part in parts[:-1])
    vector_load = vector and loads and kind is not Kind.SCALAR
    return Insn(kind, mnemonic.startswith(("j", "loop")), vector_load, first_byte == 0x62)


def disassemble(code: bytes, address: int) -> dict[int, Insn]:
    with tempfile.NamedTemporaryFile(suffix=".bin") as blob:
        blob.write(code)
        blob.flush()
        done = subprocess.run(
            ["objdump", "-D", "-b", "binary", "-m", "i386:x86-64", "--insn-width=16",
             f"--adjust-vma={address:#x}", blob.name],
            capture_output=True, text=True, check=True,
        )
    found: dict[int, Insn] = {}
    for line in done.stdout.splitlines():
        fields = line.split("\t")
        if len(fields) < 3 or not re.fullmatch(r"\s*[0-9a-f]+:", fields[0]):
            continue
        start = int(fields[0].strip()[:-1], 16)
        if start >= address + len(code) - LONGEST:
            continue
        raw = [int(byte, 16) for byte in fields[1].split()]
        first = next((byte for byte in raw if byte not in LEGACY_PREFIX_BYTES), 0)
        tokens = fields[2].split(None, 1)
        while len(tokens) > 1 and tokens[0] in PREFIXES:
            tokens = tokens[1].split(None, 1)
        if tokens:
            found[start] = decode(tokens[0], tokens[1] if len(tokens) > 1 else "", first)
    return found


def read_memory(pid: int, address: int, size: int) -> bytes:
    return b"".join((ptrace(PEEKTEXT, pid, address + offset) & WORD).to_bytes(8, "little")
                    for offset in range(0, size, 8))


def find_functions(binary: Path, base: int) -> dict[str, int]:
    listed = subprocess.run(["nm", "--defined-only", str(binary)], capture_output=True, text=True)
    if listed.returncode != 0:
        sys.exit(f"vec_check: cannot read symbols from {binary}\n{listed.stderr}")
    relocated = int.from_bytes(binary.read_bytes()[16:18], "little") == 3
    offset = base if relocated else 0
    functions = {}
    for line in listed.stdout.splitlines():
        fields = line.split()
        if len(fields) == 3 and fields[1] in "tTwW":
            functions[fields[2]] = int(fields[0], 16) + offset
    return functions


def find_image(pid: int, binary: Path) -> tuple[int, int, int]:
    spans = []
    for line in Path(f"/proc/{pid}/maps").read_text().splitlines():
        fields = line.split()
        if len(fields) >= 6 and fields[5] == str(binary):
            low, high = fields[0].split("-")
            spans.append((int(low, 16), int(high, 16), int(fields[2], 16)))
    if not spans:
        sys.exit(f"vec_check: {binary} is not mapped into its own process")
    base = min(low - offset for low, _, offset in spans)
    return base, min(low for low, _, _ in spans), max(high for _, high, _ in spans)


def launch(binary: Path, stdin: Path, stdout: int) -> int:
    env = {**os.environ, "GODEBUG": "asyncpreemptoff=1", "GOGC": "off"}
    pid = os.fork()
    if pid == 0:
        try:
            os.dup2(os.open(stdin, os.O_RDONLY), 0)
            os.dup2(stdout, 1)
            libc.prctl(SET_PDEATHSIG, ctypes.c_ulong(signal.SIGKILL))
            if libc.ptrace(TRACEME, 0, None, None) == -1:
                os._exit(REFUSED)
            os.execve(binary, [str(binary)], env)
        finally:
            os._exit(127)
    _, status = os.waitpid(pid, 0)
    if os.WIFEXITED(status) and os.WEXITSTATUS(status) == REFUSED:
        sys.exit("vec_check: this system does not permit ptrace, which the grade needs:"
                 " kernel.yama.ptrace_scope must be 0 or 1 and no seccomp filter may block it")
    if not os.WIFSTOPPED(status):
        sys.exit(f"vec_check: could not start {binary}")
    return pid


def enter(pid: int, entry: int) -> int:
    regs = Regs()
    original = ptrace(PEEKTEXT, pid, entry) & WORD
    ptrace(POKETEXT, pid, entry, (original & ~0xFF) | 0xCC)
    pending = 0
    while True:
        ptrace(CONT, pid, 0, pending)
        _, status = os.waitpid(pid, 0)
        if not os.WIFSTOPPED(status):
            code = os.waitstatus_to_exitcode(status)
            hint = "; was it inlined into its caller?" if code == 0 else ""
            sys.exit(f"vec_check: the program exited with status {code}"
                     f" without calling the graded function{hint}")
        pending = os.WSTOPSIG(status)
        if pending != signal.SIGTRAP:
            continue
        pending = 0
        ptrace(GETREGS, pid, 0, ctypes.addressof(regs))
        if regs.rip == entry + 1:
            break
    ptrace(POKETEXT, pid, entry, original)
    regs.rip = entry
    ptrace(SETREGS, pid, 0, ctypes.addressof(regs))
    return ptrace(PEEKTEXT, pid, regs.rsp) & WORD


def trace(pid: int, entry: int, morestack: int | None, image: range, scalar_limit: float) -> Count:
    returns = enter(pid, entry)
    regs = Regs()
    table: dict[int, Insn] = {}
    count = Count()
    segment = 0
    vector = False
    rip = entry
    pending = 0
    while True:
        if rip == morestack:
            rip = ptrace(PEEKTEXT, pid, regs.rsp) & WORD
            enter(pid, rip)
        insn = table.get(rip)
        if insn is None:
            table.update(disassemble(read_memory(pid, rip, WINDOW), rip))
            insn = table[rip]
        if insn.evex and rip in image:
            sys.exit(f"vec_check: AVX-512 instruction at {rip:#x}, outside x86-64-v3")
        segment += insn.kind is Kind.INTEGER
        count.scalar += insn.kind is Kind.SCALAR
        count.packed += insn.kind is Kind.PACKED
        vector |= insn.vector_load
        ptrace(SINGLESTEP, pid, 0, pending)
        _, status = os.waitpid(pid, 0)
        if not os.WIFSTOPPED(status):
            code = os.waitstatus_to_exitcode(status)
            sys.exit(f"vec_check: the program exited with status {code} inside the graded function")
        pending = os.WSTOPSIG(status)
        if pending != signal.SIGTRAP:
            continue
        pending = 0
        ptrace(GETREGS, pid, 0, ctypes.addressof(regs))
        returned = regs.rip == returns
        if returned or (insn.jump and regs.rip <= rip):
            count.scalar += 0 if vector else segment
            segment = 0
            vector = False
            if count.scalar > scalar_limit:
                return count
        rip = regs.rip
        if returned:
            count.returned = True
            return count


def strip_comments(source: str) -> str:
    source = re.sub(r"/\*.*?\*/", " ", source, flags=re.DOTALL)
    return re.sub(r"//[^\n]*", "", source)


def lint(workdir: Path) -> list[str]:
    if (workdir / "Cargo.toml").exists():
        sources = sorted((workdir / "src").rglob("*.rs"))
        banned = RUST_BANNED
        outside = [path for path in [workdir / "build.rs"] if path.exists()]
    elif (workdir / "go.mod").exists():
        sources = sorted(p for p in workdir.glob("*.go") if not p.name.endswith("_test.go"))
        banned = GO_BANNED
        outside = sorted(p for p in workdir.iterdir() if p.suffix in GO_OUTSIDE)
    else:
        sources = sorted([*workdir.glob("*.c"), *workdir.glob("*.h")])
        banned = C_BANNED
        outside = []
    problems = [f"{path.name}: compiled outside the graded build" for path in outside]
    for path in sources:
        text = strip_comments(path.read_text(encoding="utf-8"))
        problems += [f"{path.relative_to(workdir)}: {what}"
                     for pattern, what in banned if pattern.search(text)]
    return problems


def count_units(input_path: Path, key: str) -> int:
    value = json.loads(input_path.read_text(encoding="utf-8"))[key]
    return len(value.encode() if isinstance(value, str) else value)


def run(binary: Path, function: str, input_path: Path, scalar_limit: float) -> Count:
    with tempfile.TemporaryFile() as out:
        pid = launch(binary, input_path, out.fileno())
        base, low, high = find_image(pid, binary)
        functions = find_functions(binary, base)
        if function not in functions:
            sys.exit(f"vec_check: {binary} defines no function {function}")
        count = trace(pid, functions[function], functions.get(MORESTACK), range(low, high),
                      scalar_limit)
        if not count.returned:
            os.kill(pid, signal.SIGKILL)
            os.waitpid(pid, 0)
            return count
        ptrace(DETACH, pid)
        _, status = os.waitpid(pid, 0)
        code = os.waitstatus_to_exitcode(status)
        if code != 0:
            sys.exit(f"vec_check: {binary.name} exited with status {code}")
        out.seek(0)
        expected = input_path.with_suffix(".out")
        if expected.exists() and out.read().decode() != expected.read_text(encoding="utf-8"):
            sys.exit(f"vec_check: {binary.name} printed the wrong answer for {input_path.name}")
    return count


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--binary", type=Path, required=True)
    parser.add_argument("--function", required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--units", required=True,
                        help="the input field whose length is the unit of work")
    parser.add_argument("--expect", choices=("vectorized", "scalar"), required=True)
    parser.add_argument("--sources", type=Path, default=Path.cwd())
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    problems = lint(args.sources)
    for problem in problems:
        print(f"  {problem} is not allowed")
    if problems:
        sys.exit(1)

    signal.signal(signal.SIGALRM, lambda *_: sys.exit(
        f"vec_check: {args.binary.name} did not finish within {TIMEOUT} s under the tracer"))
    signal.alarm(TIMEOUT)
    units = max(count_units(args.input, args.units), 1)
    count = run(args.binary.resolve(), args.function, args.input, BUDGET * units)
    scalar = count.scalar / units
    packed = count.packed / units
    vectorized = count.returned and scalar < BUDGET and packed >= PACKED_FLOOR
    found = "vectorized" if vectorized else "scalar"
    shape = (f"{scalar:.2f} scalar, {packed:.2f} packed" if count.returned
             else f"over {BUDGET:.2f} scalar")
    ok = found == args.expect
    print(f"  {args.function}: {shape} per element of {args.units} ({units})"
          f" -> {found}{'' if ok else '  EXPECTED ' + args.expect}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()

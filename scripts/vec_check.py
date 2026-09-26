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
iteration that runs a packed instruction, or loads several elements into a
vector register in one instruction, is a vector iteration. There, loop control,
bounds checks, and mask arithmetic on general-purpose registers are paid once
per vector rather than once per element. That bookkeeping is what separates C,
Rust, and Go most; leaving it out lets one budget mean the same thing in all
three. Packed arithmetic, moves between registers, zeroing a vector register,
stack accesses, string instructions such as rep movsb, and control flow count
on neither side.

The count is divided by the challenge's unit of work, read from the input: the
length of one array or string, the value of one integer, or the product of
several, written a*b. A function is vectorized when it retires fewer than BUDGET
scalar instructions per unit and at least PACKED_FLOOR packed ones. Any scalar
pass over the input costs at least one per unit however many vector loops run
beside it: a load or a floating-point add per element. Setup, a remainder
tail, and a horizontal sum cost a fraction of one. A loop the input never runs
costs nothing. A grade that fails lists the source lines, or the libraries,
where most of the counted scalar instructions ran.

Before tracing, the solver's sources are checked for the ways to emit code the
compiler did not choose for x86-64-v3: inline or standalone assembly, pragmas
and attributes that change the target or the optimizer, Rust's
`#[target_feature]`, and build scripts and cgo that compile code outside the
graded build. While tracing, an AVX-512 instruction in the program's own code
is refused for the same reason.

Only the thread that calls the graded function is traced, so no other thread
may work while it runs. At its entry every other thread of the program is
stopped until it returns, and a program that has started another process that
is still running is refused. A traced instruction that starts a thread or a
process, a clone, clone3, fork, or vfork system call, or a goroutine, a call to
Go's runtime.newproc, is refused, and so is a futex wait, which can only wait
for a stopped thread.

The dynamic linker binds every library function when the program starts, not
at its first call, so solve is not charged for looking up a function that main
happened not to call before it.

Go's asynchronous preemption and collector are switched off. The two ways Go's
runtime moves to the thread's own stack run untraced until they resume the
function that entered them: runtime.morestack grows the goroutine's stack or
preempts it, and runtime.systemstack grows the heap among other bookkeeping.
All of it is work that is not the solver's, and how much of it runs depends on
timing and on the heap the program built before solve. The runtime can only
have asked the goroutine to yield before the other threads stopped; a detour
entered with that request pending runs with them resumed, because the yield
hands the goroutine to the scheduler on another thread and back.

The grade traces at most STEPS instructions and fails a function that runs
longer. The count decides, not the clock, so a loaded machine grades a function
as an idle one does. A program that keeps the grader waiting HANG seconds for
its next stop, blocked in a system call or running untraced code, fails as well,
and the traced program dies with the grader.
"""

from __future__ import annotations

import argparse
import bisect
import ctypes
import enum
import json
import math
import os
import re
import signal
import subprocess
import sys
import tempfile
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

BUDGET = 1.0
PACKED_FLOOR = 0.02
WINDOW = 256
LONGEST = 15
STEPS = 16_000_000
HANG = 60
PLACES = 5
DETOURS = ("runtime.morestack.abi0", "runtime.systemstack.abi0")
SPAWNS = ("runtime.newproc",)
SPAWN_SYSCALLS = {56, 57, 58, 435}  # clone, fork, vfork, clone3
FUTEX = 202
FUTEX_WAITV = 449
FUTEX_WAITS = {0, 6, 9, 11, 13}  # wait, lock_pi, wait_bitset, wait_requeue_pi, lock_pi2
GO_STACKGUARD = 16
GO_PREEMPT = 0xFFFFFFFFFFFFFADE
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
SETOPTIONS = 0x4200
GETEVENTMSG = 0x4201
SEIZE = 0x4206
INTERRUPT = 0x4207
TRACE_SPAWNS = 0x2 | 0x4 | 0x8  # fork, vfork, clone
WALL = 0x40000000
SET_PDEATHSIG = 1
SET_CHILD_SUBREAPER = 36

libc = ctypes.CDLL(None, use_errno=True)
libc.ptrace.restype = ctypes.c_long
libc.ptrace.argtypes = (ctypes.c_long, ctypes.c_long, ctypes.c_void_p, ctypes.c_void_p)


class Regs(ctypes.Structure):
    _fields_ = [
        (name, ctypes.c_ulonglong)
        for name in (
            "r15 r14 r13 r12 rbp rbx r11 r10 r9 r8 rax rcx rdx rsi rdi orig_rax "
            "rip cs eflags rsp ss fs_base gs_base ds es fs gs"
        ).split()
    ]


class Kind(enum.Enum):
    INTEGER = "integer"
    SCALAR = "scalar"
    PACKED = "packed"
    OTHER = "other"


@dataclass(frozen=True, slots=True)
class Insn:
    kind: Kind
    jump: bool
    vector_work: bool
    evex: bool
    syscall: bool


@dataclass
class Count:
    scalar: int = 0
    packed: int = 0
    steps: int = 0
    returned: bool = False
    hot: Counter[int] = field(default_factory=Counter)
    places: Counter[str] = field(default_factory=Counter)


PREFIXES = {
    "lock",
    "rep",
    "repz",
    "repe",
    "repnz",
    "repne",
    "notrack",
    "bnd",
    "data16",
    "addr32",
    "cs",
    "ds",
    "es",
    "fs",
    "gs",
    "ss",
}
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
ZEROING = re.compile(r"^v?(pxor|xorp[sd])$")

C_BANNED = [
    (re.compile(r"\b(asm|__asm__|__asm)\b"), "inline assembly"),
    (re.compile(r"^\s*#\s*pragma\b|\b_Pragma\s*\(", re.MULTILINE), "a #pragma"),
    (
        re.compile(r"\b_*(target|optimize|target_clones)_*\s*\("),
        "a target or optimize attribute",
    ),
]
RUST_BANNED = [
    (re.compile(r"\b(asm|global_asm|naked_asm)!"), "inline assembly"),
    (
        re.compile(r"#!?\[\s*(unsafe\s*\(\s*)?(target_feature|naked)\b"),
        "#[target_feature] or #[naked]",
    ),
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
    memory = any(
        "(" in part and not STACK.search(part) for part in parts
    ) and not NO_ACCESS.match(mnemonic)
    extracts = bool(parts) and GENERAL_REGISTER.match(parts[-1]) is not None
    if STRING.match(mnemonic) or (ZEROING.match(mnemonic) and len(set(parts)) == 1):
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
    return Insn(
        kind,
        mnemonic.startswith(("j", "loop")),
        vector_load or kind is Kind.PACKED,
        first_byte == 0x62,
        mnemonic == "syscall",
    )


def disassemble(code: bytes, address: int) -> dict[int, Insn]:
    with tempfile.NamedTemporaryFile(suffix=".bin") as blob:
        blob.write(code)
        blob.flush()
        done = subprocess.run(
            [
                "objdump",
                "-D",
                "-b",
                "binary",
                "-m",
                "i386:x86-64",
                "--insn-width=16",
                f"--adjust-vma={address:#x}",
                blob.name,
            ],
            capture_output=True,
            text=True,
            check=True,
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
            found[start] = decode(
                tokens[0], tokens[1] if len(tokens) > 1 else "", first
            )
    return found


def wait(pid: int) -> int:
    signal.alarm(HANG)
    _, status = os.waitpid(pid, 0)
    signal.alarm(0)
    return status


def read_memory(pid: int, address: int, size: int) -> bytes:
    return b"".join(
        (ptrace(PEEKTEXT, pid, address + offset) & WORD).to_bytes(8, "little")
        for offset in range(0, size, 8)
    )


def load_offset(binary: Path, base: int) -> int:
    relocated = int.from_bytes(binary.read_bytes()[16:18], "little") == 3
    return base if relocated else 0


def find_functions(binary: Path, offset: int) -> dict[str, int]:
    listed = subprocess.run(
        ["nm", "--defined-only", "--demangle", str(binary)],
        capture_output=True,
        text=True,
    )
    if listed.returncode != 0:
        sys.exit(f"vec_check: cannot read symbols from {binary}\n{listed.stderr}")
    functions = {}
    for line in listed.stdout.splitlines():
        fields = line.split(maxsplit=2)
        if len(fields) == 3 and fields[1] in "tTwW":
            functions[fields[2]] = int(fields[0], 16) + offset
    return functions


def read_maps(pid: int) -> list[tuple[int, int, int, str]]:
    maps = []
    for line in Path(f"/proc/{pid}/maps").read_text().splitlines():
        fields = line.split()
        if len(fields) >= 6:
            low, high = fields[0].split("-")
            maps.append((int(low, 16), int(high, 16), int(fields[2], 16), fields[5]))
    return maps


def find_image(pid: int, binary: Path) -> tuple[int, int, int]:
    spans = [
        (low, high, offset)
        for low, high, offset, path in read_maps(pid)
        if path == str(binary)
    ]
    if not spans:
        sys.exit(f"vec_check: {binary} is not mapped into its own process")
    base = min(low - offset for low, _, offset in spans)
    return base, min(low for low, _, _ in spans), max(high for _, high, _ in spans)


def read_lines(binary: Path) -> tuple[list[int], list[str | None]]:
    decoded = subprocess.run(
        ["objdump", "--dwarf=decodedline", str(binary)],
        capture_output=True,
        text=True,
    )
    rows: dict[int, str | None] = {}
    for line in decoded.stdout.splitlines():
        fields = line.split()
        if len(fields) < 3 or not fields[2].startswith("0x"):
            continue
        if fields[1].isdigit():
            rows[int(fields[2], 16)] = f"{fields[0]}:{fields[1]}"
        else:
            rows.setdefault(int(fields[2], 16), None)
    starts = sorted(rows)
    return starts, [rows[start] for start in starts]


def locate(
    pid: int, binary: Path, offset: int, functions: dict[str, int], hot: Counter[int]
) -> Counter[str]:
    maps = read_maps(pid)
    starts, lines = read_lines(binary)
    names = {address: name for name, address in functions.items()}
    entries = sorted(names)
    places: Counter[str] = Counter()
    for address, times in hot.items():
        path = next((path for low, high, _, path in maps if low <= address < high), "")
        if path != str(binary):
            places[Path(path).name or "unmapped code"] += times
            continue
        entry = bisect.bisect_right(entries, address) - 1
        function = names[entries[entry]] if entry >= 0 else f"{address - offset:#x}"
        row = bisect.bisect_right(starts, address - offset) - 1
        line = lines[row] if row >= 0 else None
        places[f"{line} {function}" if line else function] += times
    return places


def launch(binary: Path, stdin: Path, stdout: int) -> int:
    env = {
        **os.environ,
        "GODEBUG": "asyncpreemptoff=1",
        "GOGC": "off",
        "LD_BIND_NOW": "1",
    }
    pid = os.fork()
    if pid == 0:
        try:
            os.dup2(os.open(stdin, os.O_RDONLY), 0)
            os.dup2(stdout, 1)
            libc.prctl(SET_PDEATHSIG, ctypes.c_ulong(signal.SIGKILL))
            libc.prctl(SET_CHILD_SUBREAPER, ctypes.c_ulong(1))
            if libc.ptrace(TRACEME, 0, None, None) == -1:
                os._exit(REFUSED)
            os.execve(binary, [str(binary)], env)
        finally:
            os._exit(127)
    status = wait(pid)
    if os.WIFEXITED(status) and os.WEXITSTATUS(status) == REFUSED:
        sys.exit(
            "vec_check: this system does not permit ptrace, which the grade needs:"
            " kernel.yama.ptrace_scope must be 0 or 1"
            " and no seccomp filter may block it"
        )
    if not os.WIFSTOPPED(status):
        sys.exit(f"vec_check: could not start {binary}")
    return pid


def enter(pid: int, entry: int, frozen: dict[int, int]) -> int:
    regs = Regs()
    original = ptrace(PEEKTEXT, pid, entry) & WORD
    ptrace(POKETEXT, pid, entry, (original & ~0xFF) | 0xCC)
    pending = 0
    while True:
        ptrace(CONT, pid, 0, pending)
        status = wait(pid)
        if not os.WIFSTOPPED(status):
            code = os.waitstatus_to_exitcode(status)
            hint = "; was it inlined into its caller?" if code == 0 else ""
            sys.exit(
                f"vec_check: the program exited with status {code}"
                f" without calling the graded function{hint}"
            )
        pending = os.WSTOPSIG(status)
        if pending != signal.SIGTRAP:
            continue
        pending = 0
        if status >> 16:
            spawned = ctypes.c_ulong()
            ptrace(GETEVENTMSG, pid, 0, ctypes.addressof(spawned))
            os.waitpid(spawned.value, WALL)
            frozen[spawned.value] = 0
            continue
        ptrace(GETREGS, pid, 0, ctypes.addressof(regs))
        if regs.rip == entry + 1:
            break
    ptrace(POKETEXT, pid, entry, original)
    regs.rip = entry
    ptrace(SETREGS, pid, 0, ctypes.addressof(regs))
    return ptrace(PEEKTEXT, pid, regs.rsp) & WORD


def find_processes(pid: int) -> list[int]:
    children: dict[int, list[int]] = {}
    for stat in Path("/proc").glob("[0-9]*/stat"):
        try:
            state, parent = stat.read_text().rpartition(")")[2].split()[:2]
        except OSError:
            continue
        if state != "Z":
            children.setdefault(int(parent), []).append(int(stat.parent.name))
    found = []
    unseen = [pid]
    while unseen:
        spawned = children.get(unseen.pop(), [])
        found += spawned
        unseen += spawned
    return found


def freeze(pid: int, frozen: dict[int, int]) -> None:
    processes = find_processes(pid)
    for process in processes:
        try:
            os.kill(process, signal.SIGKILL)
        except ProcessLookupError:
            pass
    if processes:
        sys.exit(
            "vec_check: a process the program started runs beside solve;"
            " make vec grades single-threaded work only"
        )
    ptrace(SETOPTIONS, pid, 0, TRACE_SPAWNS)
    while True:
        tasks = {int(task.name) for task in Path(f"/proc/{pid}/task").iterdir()}
        threads = tasks - frozen.keys() - {pid}
        if not threads:
            return
        for tid in threads:
            try:
                ptrace(SEIZE, tid)
            except ProcessLookupError:
                continue
            ptrace(INTERRUPT, tid)
            _, status = os.waitpid(tid, WALL)
            if os.WIFSTOPPED(status):
                frozen[tid] = 0 if status >> 16 else os.WSTOPSIG(status)


def thaw(pid: int, frozen: dict[int, int]) -> None:
    ptrace(SETOPTIONS, pid)
    for tid, pending in frozen.items():
        ptrace(DETACH, tid, 0, pending)
    frozen.clear()


def is_preempted(pid: int, regs: Regs) -> bool:
    goroutine = ptrace(PEEKTEXT, pid, regs.fs_base - 8) & WORD
    return ptrace(PEEKTEXT, pid, goroutine + GO_STACKGUARD) & WORD == GO_PREEMPT


def trace(
    pid: int,
    entry: int,
    detours: set[int],
    spawns: set[int],
    image: range,
    frozen: dict[int, int],
    scalar_limit: float,
    step_limit: int,
) -> Count:
    returns = enter(pid, entry, frozen)
    freeze(pid, frozen)
    regs = Regs()
    table: dict[int, Insn] = {}
    count = Count()
    segment: list[int] = []
    vector = False
    rip = entry
    pending = 0
    while True:
        if rip in detours:
            preempted = is_preempted(pid, regs)
            rip = ptrace(PEEKTEXT, pid, regs.rsp) & WORD
            if preempted:
                thaw(pid, frozen)
            enter(pid, rip, frozen)
            if preempted:
                freeze(pid, frozen)
        insn = table.get(rip)
        if insn is None:
            table.update(disassemble(read_memory(pid, rip, WINDOW), rip))
            insn = table[rip]
        if insn.evex and rip in image:
            sys.exit(f"vec_check: AVX-512 instruction at {rip:#x}, outside x86-64-v3")
        if insn.syscall:
            ptrace(GETREGS, pid, 0, ctypes.addressof(regs))
        if rip in spawns or (insn.syscall and regs.rax in SPAWN_SYSCALLS):
            sys.exit(
                "vec_check: solve started a thread;"
                " make vec grades single-threaded work only"
            )
        waits = regs.rax == FUTEX_WAITV or (
            regs.rax == FUTEX and regs.rsi & 0x7F in FUTEX_WAITS
        )
        if insn.syscall and waits:
            sys.exit(
                "vec_check: solve waited for another thread;"
                " make vec grades single-threaded work only"
            )
        if insn.kind is Kind.INTEGER:
            segment.append(rip)
        elif insn.kind is Kind.SCALAR:
            count.scalar += 1
            count.hot[rip] += 1
        count.packed += insn.kind is Kind.PACKED
        vector |= insn.vector_work
        count.steps += 1
        if count.steps > step_limit:
            return count
        ptrace(SINGLESTEP, pid, 0, pending)
        status = wait(pid)
        if not os.WIFSTOPPED(status):
            code = os.waitstatus_to_exitcode(status)
            sys.exit(
                f"vec_check: the program exited with status {code}"
                " inside the graded function"
            )
        pending = os.WSTOPSIG(status)
        if pending != signal.SIGTRAP:
            continue
        pending = 0
        ptrace(GETREGS, pid, 0, ctypes.addressof(regs))
        returned = regs.rip == returns
        if returned or (insn.jump and regs.rip <= rip):
            if not vector:
                count.scalar += len(segment)
                count.hot.update(segment)
            segment = []
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
        sources = sorted(
            path for path in workdir.glob("*.go") if not path.name.endswith("_test.go")
        )
        banned = GO_BANNED
        outside = sorted(
            path for path in workdir.iterdir() if path.suffix in GO_OUTSIDE
        )
    else:
        sources = sorted([*workdir.glob("*.c"), *workdir.glob("*.h")])
        banned = C_BANNED
        outside = []
    problems = [f"{path.name}: compiled outside the graded build" for path in outside]
    for path in sources:
        text = strip_comments(path.read_text(encoding="utf-8"))
        problems += [
            f"{path.relative_to(workdir)}: {what}"
            for pattern, what in banned
            if pattern.search(text)
        ]
    return problems


def size(value: int | str | list[object]) -> int:
    if isinstance(value, int):
        return value
    return len(value.encode() if isinstance(value, str) else value)


def count_units(input_path: Path, units: str) -> int:
    fields = json.loads(input_path.read_text(encoding="utf-8"))
    return math.prod(size(fields[key]) for key in units.split("*"))


def run(
    binary: Path,
    function: str,
    input_path: Path,
    scalar_limit: float,
    step_limit: int = STEPS,
) -> Count:
    with tempfile.TemporaryFile() as out:
        pid = launch(binary, input_path, out.fileno())
        base, low, high = find_image(pid, binary)
        offset = load_offset(binary, base)
        functions = find_functions(binary, offset)
        if function not in functions:
            sys.exit(f"vec_check: {binary} defines no function {function}")
        detours = {functions[name] for name in DETOURS if name in functions}
        spawns = {functions[name] for name in SPAWNS if name in functions}
        frozen: dict[int, int] = {}
        count = trace(
            pid,
            functions[function],
            detours,
            spawns,
            range(low, high),
            frozen,
            scalar_limit,
            step_limit,
        )
        thaw(pid, frozen)
        count.places = locate(pid, binary, offset, functions, count.hot)
        if not count.returned:
            os.kill(pid, signal.SIGKILL)
            wait(pid)
            return count
        ptrace(DETACH, pid)
        status = wait(pid)
        code = os.waitstatus_to_exitcode(status)
        if code != 0:
            sys.exit(f"vec_check: {binary.name} exited with status {code}")
        out.seek(0)
        expected = input_path.with_suffix(".out")
        if not expected.exists():
            return count
        if out.read().decode() != expected.read_text(encoding="utf-8"):
            sys.exit(
                f"vec_check: {binary.name} printed the wrong answer"
                f" for {input_path.name}"
            )
    return count


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--binary", type=Path, required=True)
    parser.add_argument("--function", required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument(
        "--units",
        required=True,
        help="the unit of work: an input field's length or integer value, or a*b",
    )
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

    signal.signal(
        signal.SIGALRM,
        lambda *_: sys.exit(
            f"vec_check: {args.binary.name} kept the tracer waiting {HANG} s"
            " for its next stop"
        ),
    )
    units = max(count_units(args.input, args.units), 1)
    count = run(args.binary.resolve(), args.function, args.input, BUDGET * units)
    if count.steps > STEPS:
        sys.exit(
            f"vec_check: {args.function} ran more than {STEPS:,} instructions,"
            " the most the grade traces"
        )
    scalar = count.scalar / units
    packed = count.packed / units
    vectorized = count.returned and scalar < BUDGET and packed >= PACKED_FLOOR
    found = "vectorized" if vectorized else "scalar"
    shape = (
        f"{scalar:.2f} scalar, {packed:.2f} packed"
        if count.returned
        else f"over {BUDGET:.2f} scalar"
    )
    ok = found == args.expect
    print(
        f"  {args.function}: {shape} per element of {args.units} ({units})"
        f" -> {found}{'' if ok else '  EXPECTED ' + args.expect}"
    )
    if not ok and count.places:
        first = "" if count.returned else "first "
        print(f"  where its {first}{count.scalar:,} scalar instructions ran:")
        for place, times in count.places.most_common(PLACES):
            print(f"  {times:>10,}  {place}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()

"""Benchmark one solver against ephemeral deterministic large cases."""

from __future__ import annotations

import argparse
import os
import signal
import subprocess
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path

from large_cases import Case, get_cases, write_case

ROOT = Path(__file__).resolve().parents[1]
TMP = ROOT / "tmp"


@dataclass(frozen=True, slots=True)
class Result:
    code: int
    elapsed_ms: int
    stderr: str
    timed_out: bool


def run(
    command: list[str],
    workdir: Path,
    input_path: Path,
    output_path: Path,
    timeout: float,
) -> Result:
    started = time.monotonic_ns()
    with input_path.open("rb") as stdin, output_path.open("wb") as stdout:
        process = subprocess.Popen(
            command,
            cwd=workdir,
            stdin=stdin,
            stdout=stdout,
            stderr=subprocess.PIPE,
            start_new_session=True,
        )
        try:
            _, stderr = process.communicate(timeout=timeout)
            timed_out = False
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGTERM)
            try:
                _, stderr = process.communicate(timeout=2)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                _, stderr = process.communicate()
            timed_out = True
    elapsed_ms = (time.monotonic_ns() - started) // 1_000_000
    return Result(
        code=process.returncode,
        elapsed_ms=elapsed_ms,
        stderr=stderr.decode(errors="replace"),
        timed_out=timed_out,
    )


def files_equal(left: Path, right: Path) -> bool:
    if left.stat().st_size != right.stat().st_size:
        return False
    with left.open("rb") as left_file, right.open("rb") as right_file:
        while chunk := left_file.read(1024 * 1024):
            if chunk != right_file.read(len(chunk)):
                return False
    return True


def temp_path(label: str) -> Path:
    descriptor, raw_path = tempfile.mkstemp(prefix=f"bench-{label}-", dir=TMP)
    os.close(descriptor)
    return Path(raw_path)


def report_error(label: str, result: Result) -> None:
    print(f"{label}  ERROR (exit {result.code})")
    if result.stderr:
        print(result.stderr[-4_000:].rstrip())


def benchmark_case(
    case: Case,
    command: list[str],
    workdir: Path,
    timeout: float,
    oracle_timeout: float,
    expect_timeout: bool,
) -> str | None:
    input_path = temp_path("input")
    expected_path = temp_path("expected")
    actual_path = temp_path("actual")
    try:
        with input_path.open("w", encoding="utf-8") as output:
            write_case(case, output)
        label = f"{case.name} (seed {case.seed}):"

        if not expect_timeout:
            oracle = run(
                ["uv", "run", "python", "main.py"],
                ROOT / case.challenge / "golden",
                input_path,
                expected_path,
                oracle_timeout,
            )
            if oracle.timed_out:
                print(f"{label:<48} ORACLE TIMEOUT ({oracle_timeout:g}s)")
                return "error"
            if oracle.code != 0:
                report_error(f"{label} oracle", oracle)
                return "error"

        deadline = time.monotonic() + timeout
        elapsed_ms = 0
        for repeat in range(1, case.repeats + 1):
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                result = Result(0, elapsed_ms, "", True)
            else:
                result = run(command, workdir, input_path, actual_path, remaining)
                elapsed_ms += result.elapsed_ms
            if result.timed_out:
                detail = f"repeat {repeat}/{case.repeats}" if case.repeats > 1 else ""
                if expect_timeout:
                    print(f"{label:<48} TIMEOUT ok {detail}".rstrip())
                    return None
                print(f"{label:<48} TIMEOUT (limit {timeout:g}s) {detail}".rstrip())
                return "timeout"
            if result.code != 0:
                report_error(label, result)
                return "error"
            if not expect_timeout and not files_equal(expected_path, actual_path):
                print(f"{label:<48} WRONG ANSWER (repeat {repeat}/{case.repeats})")
                return "wrong-answer"

        run_count = f", {case.repeats} runs" if case.repeats > 1 else ""
        if expect_timeout:
            print(f"{label:<48} NO TIMEOUT ({elapsed_ms}ms{run_count})")
            return "no-timeout"
        print(f"{label:<48} {elapsed_ms}ms{run_count}")
        return None
    finally:
        input_path.unlink(missing_ok=True)
        expected_path.unlink(missing_ok=True)
        actual_path.unlink(missing_ok=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--challenge")
    parser.add_argument("--workdir", type=Path, default=Path.cwd())
    parser.add_argument("--timeout", type=float, required=True)
    parser.add_argument("--oracle-timeout", type=float, default=30)
    parser.add_argument("--expect-timeout", action="store_true")
    parser.add_argument("program", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if args.program and args.program[0] == "--":
        args.program = args.program[1:]
    if not args.program:
        parser.error("a program is required after --")
    return args


def main() -> None:
    args = parse_args()
    workdir = args.workdir.resolve()
    challenge = args.challenge or workdir.parent.name
    TMP.mkdir(exist_ok=True)

    failures = []
    for case in get_cases(challenge):
        failure = benchmark_case(
            case,
            args.program,
            workdir,
            args.timeout,
            args.oracle_timeout,
            args.expect_timeout,
        )
        if failure is not None:
            failures.append(failure)
    if "timeout" in failures:
        raise SystemExit(124)
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

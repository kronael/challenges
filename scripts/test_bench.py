from __future__ import annotations

import os
import signal
import sys
import tempfile
import time
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import bench
from large_cases import Case


class RunTests(unittest.TestCase):
    def setUp(self) -> None:
        bench.TMP.mkdir(exist_ok=True)

    def test_timeout_does_not_wait_for_escaped_stderr_holder(self) -> None:
        with tempfile.TemporaryDirectory(dir=bench.TMP) as raw_dir:
            temp_dir = Path(raw_dir)
            pid_path = temp_dir / "child.pid"
            input_path = temp_dir / "input"
            output_path = temp_dir / "output"
            input_path.touch()
            code = """
import signal
import subprocess
import sys
import time
from pathlib import Path

child = subprocess.Popen(
    [sys.executable, "-c", "import time; time.sleep(3)"],
    start_new_session=True,
)
Path(sys.argv[1]).write_text(str(child.pid), encoding="utf-8")
signal.signal(signal.SIGTERM, signal.SIG_IGN)
time.sleep(10)
"""
            started = time.monotonic()
            result = bench.run(
                [sys.executable, "-c", code, str(pid_path)],
                temp_dir,
                input_path,
                output_path,
                0.1,
            )
            elapsed = time.monotonic() - started
            child_pid = int(pid_path.read_text(encoding="utf-8"))
            self.addCleanup(self.stop_process, child_pid)

            self.assertTrue(result.timed_out)
            self.assertLess(elapsed, 2.8)

    def test_early_nonzero_exit_is_not_a_timeout(self) -> None:
        with tempfile.TemporaryDirectory(dir=bench.TMP) as raw_dir:
            temp_dir = Path(raw_dir)
            pid_path = temp_dir / "child.pid"
            input_path = temp_dir / "input"
            output_path = temp_dir / "output"
            input_path.touch()
            code = """
import subprocess
import sys
from pathlib import Path

child = subprocess.Popen(
    [sys.executable, "-c", "import time; time.sleep(0.6)"],
    start_new_session=True,
)
Path(sys.argv[1]).write_text(str(child.pid), encoding="utf-8")
raise SystemExit(7)
"""
            result = bench.run(
                [sys.executable, "-c", code, str(pid_path)],
                temp_dir,
                input_path,
                output_path,
                0.1,
            )
            child_pid = int(pid_path.read_text(encoding="utf-8"))
            self.addCleanup(self.stop_process, child_pid)

            self.assertEqual(result.code, 7)
            self.assertFalse(result.timed_out)

    def stop_process(self, pid: int) -> None:
        try:
            os.kill(pid, signal.SIGTERM)
        except ProcessLookupError:
            return
        deadline = time.monotonic() + 1
        while time.monotonic() < deadline:
            try:
                os.kill(pid, 0)
            except ProcessLookupError:
                return
            stat_path = Path(f"/proc/{pid}/stat")
            try:
                is_zombie = (
                    stat_path.exists() and stat_path.read_text().split()[2] == "Z"
                )
            except ProcessLookupError:
                return
            if is_zombie:
                return
            time.sleep(0.01)
        try:
            os.kill(pid, signal.SIGKILL)
        except ProcessLookupError:
            pass


class OutputTests(unittest.TestCase):
    def setUp(self) -> None:
        bench.TMP.mkdir(exist_ok=True)

    def test_output_must_be_exactly_one_terminated_line(self) -> None:
        with tempfile.TemporaryDirectory(dir=bench.TMP) as raw_dir:
            output_path = Path(raw_dir) / "output"
            for output, expected in (
                (b"", False),
                (b"answer", False),
                (b"answer\n", True),
                (b"answer\nextra\n", False),
            ):
                with self.subTest(output=output):
                    output_path.write_bytes(output)
                    self.assertEqual(bench.has_one_output_line(output_path), expected)


class TemporaryPathTests(unittest.TestCase):
    def setUp(self) -> None:
        bench.TMP.mkdir(exist_ok=True)

    def test_partial_allocation_failure_cleans_created_paths(self) -> None:
        with tempfile.TemporaryDirectory(dir=bench.TMP) as raw_dir:
            temp_dir = Path(raw_dir)
            created_path = temp_dir / "created"
            calls = 0

            def create_path(label: str) -> Path:
                nonlocal calls
                del label
                calls += 1
                if calls == 2:
                    raise OSError("allocation failed")
                created_path.touch()
                return created_path

            case = Case("02-easy-mod-exp", "09_large_exp", 201)
            with (
                patch("bench.temp_path", side_effect=create_path),
                self.assertRaisesRegex(OSError, "allocation failed"),
            ):
                bench.benchmark_case(
                    case,
                    [sys.executable, "-c", "print(1)"],
                    temp_dir,
                    1,
                    1,
                    False,
                )

            self.assertFalse(created_path.exists())


class BenchmarkCaseTests(unittest.TestCase):
    def setUp(self) -> None:
        bench.TMP.mkdir(exist_ok=True)
        self.case = Case("02-easy-mod-exp", "09_large_exp", 201)

    def test_silent_oracle_is_rejected(self) -> None:
        def run_silently(
            command: list[str],
            workdir: Path,
            input_path: Path,
            output_path: Path,
            timeout: float,
        ) -> bench.Result:
            del command, workdir, input_path, output_path, timeout
            return bench.Result(0, 1, "", False)

        output = StringIO()
        with patch("bench.run", side_effect=run_silently), redirect_stdout(output):
            failure = bench.benchmark_case(
                self.case,
                [sys.executable, "-c", "print(1)"],
                bench.TMP,
                1,
                1,
                False,
            )

        self.assertEqual(failure, "error")
        self.assertIn("ORACLE OUTPUT", output.getvalue())

    def test_expected_timeout_rejects_early_runtime_error(self) -> None:
        def fail_early(
            command: list[str],
            workdir: Path,
            input_path: Path,
            output_path: Path,
            timeout: float,
        ) -> bench.Result:
            del command, workdir, input_path, output_path, timeout
            return bench.Result(7, 1, "broken", False)

        output = StringIO()
        with patch("bench.run", side_effect=fail_early), redirect_stdout(output):
            failure = bench.benchmark_case(
                self.case,
                [sys.executable, "-c", "raise SystemExit(7)"],
                bench.TMP,
                1,
                1,
                True,
            )

        self.assertEqual(failure, "error")
        self.assertIn("ERROR (exit 7)", output.getvalue())

    def test_silent_solver_is_rejected(self) -> None:
        calls = 0

        def run_with_silent_solver(
            command: list[str],
            workdir: Path,
            input_path: Path,
            output_path: Path,
            timeout: float,
        ) -> bench.Result:
            nonlocal calls
            del command, workdir, input_path, timeout
            calls += 1
            if calls == 1:
                output_path.write_text("answer\n", encoding="utf-8")
            return bench.Result(0, 1, "", False)

        output = StringIO()
        with (
            patch("bench.run", side_effect=run_with_silent_solver),
            redirect_stdout(output),
        ):
            failure = bench.benchmark_case(
                self.case,
                [sys.executable, "-c", "pass"],
                bench.TMP,
                1,
                1,
                False,
            )

        self.assertEqual(failure, "wrong-answer")
        self.assertIn("INVALID OUTPUT", output.getvalue())


if __name__ == "__main__":
    unittest.main()

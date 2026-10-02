"""Offline effective runtime, login shell, cache and coverage regressions."""

import importlib.util
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "runtime_tests_suite", ROOT / "benchmarks/run_benchmark.py"
)
suite = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(suite)
h = suite.harness


class CoverageTests(unittest.TestCase):
    def test_terse_unittest_footer_recovers_counts_without_inventing_identities(self):
        for output, expected in [
            ("Ran 5 tests in 0.1s\n\nOK\n", (5, 0, 0, 0)),
            ("Ran 5 tests in 0.1s\n\nFAILED (failures=1, errors=1, skipped=1)\n", (2, 1, 1, 1)),
        ]:
            record = suite.trace.coverage("python3 -m unittest", output)
            self.assertEqual(
                tuple(
                    record[k]
                    for k in ["passed_count", "failed_count", "error_count", "skipped_count"]
                ),
                expected,
            )
            self.assertTrue(record["status_counts_complete"])
            self.assertFalse(record["test_list_complete"])
            self.assertEqual(record["test_names"], [])
            self.assertIsNone(record["normalized_test_list_sha256"])

    def test_real_v3_modern_and_older_output_recovers_same_complete_set(self):
        examples = json.loads(
            (ROOT / "tests/fixtures/benchmark/v3-unittest-output.json").read_text()
        )
        records = [suite.trace.coverage(e["command"], e["output"]) for e in examples]
        self.assertEqual([r["discovered_count"] for r in records], [5, 0, 5, 6])
        for record in [records[0], records[2], records[3]]:
            self.assertTrue(record["passed"])
            self.assertTrue(record["test_list_complete"])
            self.assertEqual(record["passed_count"], record["discovered_count"])
            self.assertEqual(record["failed_count"], 0)
            self.assertEqual(record["error_count"], 0)
            self.assertEqual(record["skipped_count"], 0)
            self.assertEqual(len(record["test_names"]), record["discovered_count"])
        self.assertEqual(
            records[0]["normalized_test_list_sha256"], records[2]["normalized_test_list_sha256"]
        )
        self.assertIn("test_expenses.ExpenseTests.test_filter", records[0]["test_names"])
        self.assertIsNone(records[1]["normalized_test_list_sha256"])

    def test_order_and_invocation_are_irrelevant_but_incomplete_is_explicit(self):
        rows = ["test_a (test_demo.Suite) ... ok", "test_b (test_demo.Suite) ... skipped 'reason'"]
        first = suite.trace.coverage(
            "python3 -m unittest discover -v", "\n".join(rows) + "\nRan 2 tests\nOK (skipped=1)\n"
        )
        second = suite.trace.coverage(
            "python3 -m unittest tests.test_demo -v",
            "\n".join(
                reversed(
                    [
                        r.replace(
                            "(test_demo.Suite)", "(tests.test_demo.Suite." + r.split()[0] + ")"
                        )
                        for r in rows
                    ]
                )
            )
            + "\nRan 2 tests\nOK (skipped=1)\n",
        )
        self.assertEqual(
            first["normalized_test_list_sha256"], second["normalized_test_list_sha256"]
        )
        self.assertEqual(first["skipped_count"], 1)
        for output in [
            "Ran 2 tests\nOK\n",
            rows[0] + "\nRan 2 tests\n",
            rows[0] + "\nRan 1 test\nRan 1 test\n",
        ]:
            record = suite.trace.coverage("python3 -m unittest -v", output)
            self.assertFalse(record["test_list_complete"])
            self.assertIsNone(record["normalized_test_list_sha256"])
        record = suite.trace.coverage(
            "python3 -m unittest -v",
            "test_a (mod.Suite) ... FAIL\ntest_b (mod.Suite.test_b) ... ERROR\nRan 2 tests\nFAILED (failures=1, errors=1)\n",
        )
        self.assertEqual(
            (
                record["passed_count"],
                record["failed_count"],
                record["error_count"],
                record["skipped_count"],
            ),
            (0, 1, 1, 0),
        )
        self.assertFalse(record["passed"])


class RuntimeTests(unittest.TestCase):
    def test_runtime_pinning_does_not_inherit_host_git_helper_or_configuration(self):
        with patch.dict(
            os.environ,
            {
                "GIT_EXEC_PATH": "/uncontrolled/host/helpers",
                "GIT_CONFIG_GLOBAL": "/uncontrolled/host/config",
            },
        ):
            runtime = h.pin_runtime(shutil.which("python3"), "/bin/sh")
        self.assertNotEqual(runtime["binaries"]["git"]["exec_path"], "/uncontrolled/host/helpers")

    def test_direct_shims_and_shell_startup_ignore_host_environment(self):
        shell = shutil.which("zsh") or shutil.which("bash")
        if not shell:
            self.skipTest("login-shell regression requires zsh or bash")
        runtime = h.pin_runtime(shutil.which("python3"), shell)
        with tempfile.TemporaryDirectory() as tmp:
            receipts = []
            for condition in ["vanilla", "contextlean"]:
                with h.session_root(
                    runtime,
                    h.environment_source(
                        "codex",
                        {
                            "PATH": "/host/bad",
                            "HOME": "/host/home",
                            "ZDOTDIR": "/host/config",
                            "PYTHONPATH": "/host/python",
                        },
                    ),
                    Path(tmp),
                ) as session:
                    (session.repo / "example").write_text("same baseline")
                    h.initialize_git(session)
                    # Simulate /etc/zprofile's system-first PATH and a host
                    # user startup file. The session never sources this home.
                    host = Path(tmp) / condition
                    host.mkdir()
                    (host / ".zprofile").write_text("export PATH=/usr/bin:/bin\n")
                    env = dict(session.env, PATH="/usr/bin:/bin:" + session.env["PATH"])
                    result = subprocess.run(
                        h.runtime_control.shell_command(
                            session,
                            "command -v python3; python3 --version; command -v git; command -v rg",
                        ),
                        cwd=session.repo,
                        env=env,
                        capture_output=True,
                        text=True,
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(result.stderr, "")
                    self.assertEqual(
                        result.stdout.splitlines()[0], str(session.root / "cache/bin/python3")
                    )
                    self.assertIn(runtime["binaries"]["python3"]["version"], result.stdout)
                    for name in ["python3", "git", "rg"]:
                        shim = (session.root / "cache/bin" / name).read_text()
                        self.assertIn("exec " + runtime["binaries"][name]["path"], shim)
                        self.assertNotIn("exec " + str(session.root / "cache/bin"), shim)
                    receipt = h.runtime_control.probe(session, lambda command: command)
                    self.assertTrue(receipt["passed"], receipt["errors"])
                    receipts.append(session.sanitizer.value(receipt["effective"]))
                self.assertTrue(session.cleanup_verified)
            self.assertEqual(*receipts)

    def test_runtime_mismatch_cannot_authorize_model_and_saves_failed_receipt(self):
        runtime = h.pin_runtime(shutil.which("python3"), "/bin/sh")
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            with h.session_root(runtime, h.environment_source("codex", {}), output) as session:
                policy = dict(
                    h.execution.strategy("codex"),
                    provider="codex",
                    native_preflight=True,
                    permission_probe={"passed": True},
                    native_sandbox_available=True,
                )
                with (
                    patch.object(
                        h.runtime_control,
                        "probe",
                        return_value={"passed": False, "errors": ["effective python3 mismatch"]},
                    ),
                    patch.object(h, "execute_session") as launch,
                ):
                    with self.assertRaisesRegex(h.HarnessError, "effective python3 mismatch"):
                        h.effective_runtime_preflight(session, policy, output)
                    with self.assertRaises(h.HarnessError):
                        h.execution_command(session, policy, ["DO-NOT-LAUNCH"], output)
                    launch.assert_not_called()
                self.assertFalse(
                    json.loads(next((output / "preflight").glob("*-runtime.json")).read_text())[
                        "passed"
                    ]
                )
            self.assertTrue(session.cleanup_verified)


@unittest.skipUnless(
    platform.system() == "Darwin" and shutil.which("codex"),
    "real macOS native-runtime assertion requires macOS and installed Codex; generic controls still run",
)
class NativeRuntimeTests(unittest.TestCase):
    def test_native_login_shell_runtime_cache_permissions_and_condition_parity(self):
        runtime = h.pin_runtime("codex", "/bin/zsh")
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            receipts = []
            for condition in ["vanilla", "contextlean"]:
                with h.session_root(runtime, h.environment_source("codex", {}), output) as session:
                    (session.repo / "example").write_text(condition)
                    baseline = h.initialize_git(session)
                    policy = h.permission_preflight(
                        session, h.permission_policy(session, "codex", "workspace-write"), output
                    )
                    receipt = h.effective_runtime_preflight(session, policy, output)
                    self.assertTrue(receipt["passed"])
                    self.assertEqual(receipt["stderr"], "")
                    self.assertEqual(receipt["effective"]["git_config"]["stderr"], "")
                    self.assertTrue(all(receipt["effective"]["cache_writes"].values()))
                    self.assertNotIn("couldn't create cache file", receipt["stdout"])
                    self.assertEqual(
                        policy["permission_probe"]["operations"]["outside_write"], False
                    )
                    self.assertEqual(h.git_state(session), baseline)
                    receipts.append(session.sanitizer.value(receipt))
                self.assertTrue(session.cleanup_verified)
            self.assertEqual(*receipts)

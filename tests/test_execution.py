"""No model calls: provider strategy guards and real offline CLI sandbox probes."""

import importlib.util
import json
from pathlib import Path
import platform
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location(
    "execution_suite_tests", Path(__file__).resolve().parents[1] / "benchmarks/run_benchmark.py"
)
suite = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(suite)
h = suite.harness
execution = h.execution


class StrategyTests(unittest.TestCase):
    def test_provider_strategies_are_explicit_and_cannot_be_downgraded(self):
        for provider in ["codex", "claude", "external"]:
            policy = dict(execution.strategy(provider), provider=provider)
            execution.validate_strategy(policy)
            self.assertNotEqual(policy["provider_native_sandbox"], policy["outer_os_sandbox"])
            for field in ["provider_native_sandbox", "outer_os_sandbox", "execution_strategy"]:
                with self.assertRaises(execution.ExecutionError):
                    execution.validate_strategy(dict(policy, **{field: None}))
        with self.assertRaises(execution.ExecutionError):
            execution.strategy("unknown")

    def test_nested_mode_is_rejected_before_subprocess_or_model_invocation(self):
        policy = dict(
            execution.strategy("codex"),
            provider="codex",
            outer_os_sandbox=True,
            native_preflight=True,
        )
        with patch.object(h.subprocess, "run") as launch:
            with self.assertRaisesRegex(h.HarnessError, "nested"):
                h.execution_command(None, policy, ["DO-NOT-LAUNCH"], None)
            with self.assertRaisesRegex(h.HarnessError, "nested"):
                h.boundary_command(None, policy, ["DO-NOT-LAUNCH"], None)
            launch.assert_not_called()

    def test_unverified_provider_or_missing_probe_fails_closed(self):
        for provider in ["claude", "codex"]:
            policy = dict(execution.strategy(provider), provider=provider)
            with self.assertRaises(execution.ExecutionError):
                execution.model_command(policy, ["DO-NOT-LAUNCH"])

    def test_codex_exec_and_offline_probe_share_one_native_profile(self):
        runtime = h.pin_runtime(shutil.which("python3"), "/bin/sh")
        with tempfile.TemporaryDirectory() as tmp:
            with h.session_root(runtime, h.environment_source("codex", {}), Path(tmp)) as session:
                policy = h.permission_policy(session, "codex", "workspace-write")
                native = execution.native_command(session, policy, ["local-command"])
                invocation = h.invocation(
                    session, "codex", "offline-test", "high", "workspace-write", policy
                )
                common = execution.codex_options(session, policy)
                offset = invocation.index(common[1]) - 1
                self.assertEqual(invocation[offset : offset + len(common)], common)
                self.assertIn("--include-managed-config", native)
                self.assertNotIn("--sandbox", invocation)
                self.assertNotIn("--dangerously-bypass-approvals-and-sandbox", invocation)
                self.assertIn('":root"="deny"', common[3])
                self.assertIn('"network"={"enabled"=false}', common[3])
                policy["native_preflight"] = {"harness_only": True}
                with self.assertRaises(execution.ExecutionError):
                    execution.model_command(policy, invocation)

    def test_native_probe_failure_preserves_receipt_and_does_not_launch_model(self):
        runtime = h.pin_runtime(shutil.which("python3"), "/bin/sh")
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            with h.session_root(runtime, h.environment_source("codex", {}), output) as session:
                policy = h.permission_policy(session, "codex", "workspace-write")
                failed = subprocess.CompletedProcess(
                    [], 71, "", "sandbox_apply: Operation not permitted"
                )
                with patch.object(execution.subprocess, "run", return_value=failed) as probe:
                    with self.assertRaisesRegex(h.HarnessError, "compatibility preflight failed"):
                        h.permission_preflight(session, policy, output)
                    self.assertEqual(probe.call_count, 1)
                    self.assertIn("sandbox", probe.call_args.args[0])
                receipt = json.loads(
                    next((output / "preflight").glob("*-permission.json")).read_text()
                )
                self.assertFalse(receipt["permission_probe"]["passed"])
                self.assertEqual(receipt["permission_probe"]["exit_code"], 71)
                self.assertFalse(receipt["native_sandbox_available"])
                with self.assertRaises(h.HarnessError):
                    h.execution_command(session, policy, ["DO-NOT-LAUNCH"], output)
            self.assertTrue(session.cleanup_verified)

    def test_claude_primitive_diagnostic_cannot_authorize_native_cli(self):
        runtime = h.pin_runtime(shutil.which("python3"), "/bin/sh")
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            with h.session_root(runtime, h.environment_source("claude", {}), output) as session:
                policy = dict(
                    execution.strategy("claude"),
                    provider="claude",
                    sandbox="workspace-write",
                    primitive_backend="sandbox-exec",
                    native_preflight=None,
                )
                result = subprocess.CompletedProcess(
                    [], 0, "[true,true,false,false,false,false]", ""
                )
                with (
                    patch.object(execution.subprocess, "run", return_value=result),
                    patch.object(h, "outer_command", return_value=["primitive-only"]),
                ):
                    with self.assertRaisesRegex(h.HarnessError, "primitive-only"):
                        h.permission_preflight(session, policy, output)
                self.assertTrue(policy["permission_probe"]["primitive_passed"])
                self.assertFalse(policy["permission_probe"]["passed"])
                self.assertIsNone(policy["native_sandbox_available"])
                self.assertIn("unverified", policy["probe_scope"])
                with self.assertRaises(h.HarnessError):
                    h.execution_command(session, policy, ["DO-NOT-LAUNCH"], output)


@unittest.skipUnless(
    platform.system() == "Darwin" and Path("/usr/bin/sandbox-exec").exists(),
    "exact nested Seatbelt assertion requires macOS sandbox-exec",
)
class MacOSCompositionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not shutil.which("codex"):
            raise unittest.SkipTest(
                "offline native CLI regression requires installed Codex; generic guards still run"
            )
        cls.runtime = h.pin_runtime("codex")

    def test_native_permissions_parity_readonly_and_scratch_invisibility(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            receipts = []
            old_scratch = None
            for condition in ["vanilla", "contextlean"]:
                with h.session_root(
                    self.runtime, h.environment_source("codex", {}), output
                ) as session:
                    policy = h.permission_preflight(
                        session, h.permission_policy(session, "codex", "workspace-write"), output
                    )
                    receipts.append(session.sanitizer.value(policy))
                    self.assertEqual(
                        policy["permission_probe"]["operations"],
                        {
                            "repo_write": True,
                            "tmp_write": True,
                            "parent_write": False,
                            "outside_write": False,
                            "evidence_read": False,
                            "outside_read": False,
                        },
                    )
                    scratch = session.tmp / "previous-session-secret"
                    scratch.write_text(condition)
                    if old_scratch:
                        self.assertFalse(old_scratch.exists())
                        result = subprocess.run(
                            h.boundary_command(
                                session,
                                policy,
                                [
                                    self.runtime["binaries"]["python3"]["path"],
                                    "-c",
                                    "import pathlib,sys;print(pathlib.Path(sys.argv[1]).exists())",
                                    str(old_scratch),
                                ],
                                output,
                            ),
                            cwd=session.repo,
                            env=session.env,
                            capture_output=True,
                            text=True,
                            check=False,
                        )
                        self.assertEqual(result.returncode, 0)
                        self.assertEqual(result.stdout.strip(), "False")
                    old_scratch = scratch
                    old_root = session.root
                self.assertTrue(session.cleanup_verified)
                self.assertFalse(old_root.exists())
            h.compare_receipts(*receipts, "permission")
            with h.session_root(self.runtime, h.environment_source("codex", {}), output) as session:
                policy = h.permission_preflight(
                    session, h.permission_policy(session, "codex", "read-only"), output
                )
                self.assertFalse(policy["native_preflight"]["repo_write"])
                self.assertTrue(policy["native_preflight"]["tmp_write"])

    def test_original_boundary_reproduces_exit71_and_repaired_path_exits_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            with h.session_root(self.runtime, h.environment_source("codex", {}), output) as session:
                policy = h.permission_preflight(
                    session, h.permission_policy(session, "codex", "workspace-write"), output
                )
                native = h.boundary_command(
                    session,
                    policy,
                    [
                        self.runtime["binaries"]["python3"]["path"],
                        "-c",
                        "print('offline nested sandbox probe')",
                    ],
                    output,
                )
                result = subprocess.run(
                    native,
                    cwd=session.repo,
                    env=session.env,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                diagnostic = dict(policy, backend="sandbox-exec")
                nested = h.outer_command(session, diagnostic, native, output)
                result = subprocess.run(
                    nested,
                    cwd=session.repo,
                    env=session.env,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(result.returncode, 71, result.stderr)
                self.assertIn("sandbox_apply: Operation not permitted", result.stderr)
                with patch.object(h.subprocess, "run") as launch:
                    with self.assertRaisesRegex(h.HarnessError, "nested"):
                        h.execution_command(
                            session, dict(policy, outer_os_sandbox=True), ["DO-NOT-LAUNCH"], output
                        )
                    launch.assert_not_called()

    def test_other_live_session_scratch_is_unreadable(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            with h.session_root(self.runtime, h.environment_source("codex", {}), output) as first:
                scratch = first.tmp / "secret"
                scratch.write_text("must remain private")
                with h.session_root(
                    self.runtime, h.environment_source("codex", {}), output
                ) as second:
                    policy = h.permission_preflight(
                        second, h.permission_policy(second, "codex", "workspace-write"), output
                    )
                    command = [
                        self.runtime["binaries"]["python3"]["path"],
                        "-c",
                        "import pathlib,sys;pathlib.Path(sys.argv[1]).read_bytes()",
                        str(scratch),
                    ]
                    result = subprocess.run(
                        h.boundary_command(second, policy, command, output),
                        cwd=second.repo,
                        env=second.env,
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("PermissionError", result.stderr)
                self.assertTrue(second.cleanup_verified)
            self.assertTrue(first.cleanup_verified)

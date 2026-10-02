"""Harness contracts. Real filesystem/Git probes; synthetic provider events only."""

import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "suite_v2_tests", ROOT / "benchmarks/run_benchmark.py"
)
suite = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(suite)
h, trace = suite.harness, suite.trace


def offline_runtime():
    # A fake CLI is never called except --version. All actual task binaries are
    # pinned normally; tests that mock the launch boundary do not contact a model.
    runtime = h.pin_runtime(sys.executable, "/bin/sh")
    return runtime


def test_env():
    return h.environment_source("codex", {"OPENAI_API_KEY": "offline-only-secret"})


def prepare_receipt(path):
    review = {
        "semantics_reviewed": True,
        "entries": {
            name: {
                "responsibility": description,
                "evidence": [{"path": name, "contains": (suite.FIXTURE / name).read_text()}],
            }
            for name, description in suite.preparation.project_map(suite.FIXTURE).items()
        },
    }
    suite.core.write_json(path, suite.preparation.validate(suite.FIXTURE, review, suite.FIXTURE))


def args_for(tmp, **overrides):
    args = dict(
        model="offline-test",
        reasoning="low",
        repeat=1,
        timeout=10,
        tasks_file=suite.TASKS,
        output_dir=tmp / "output",
        codex=sys.executable,
        preparation_record=tmp / "preparation.json",
        live=True,
    )
    args.update(overrides)
    return suite.argparse.Namespace(**args)


def fake_permission(session, policy, output):
    policy["native_preflight"] = {"mocked_for_runner_test": True}
    return policy


class IsolationTests(unittest.TestCase):
    def test_parent_scratch_is_destroyed_and_invisible_to_next_session(self):
        runtime = offline_runtime()
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            with h.session_root(runtime, test_env(), output) as a:
                scratch = a.root / "scratch-above-repo.py"
                scratch.write_text("private session A state")
                a_root = a.root
                self.assertTrue(scratch.exists())
            self.assertTrue(a.cleanup_verified)
            self.assertFalse(a_root.exists())
            with h.session_root(runtime, test_env(), output) as b:
                self.assertNotEqual(a_root, b.root)
                self.assertEqual(b.env["HOME"], str(b.tmp / "home"))
                self.assertEqual(b.env["PYTHONNOUSERSITE"], "1")
                self.assertFalse(scratch.exists())
                self.assertFalse((b.root / scratch.name).exists())
                self.assertEqual(
                    set(p.name for p in b.root.iterdir()),
                    {"repo", "tmp", "cache", "artifacts", "receipts"},
                )
            self.assertTrue(b.cleanup_verified)

    def test_exception_also_destroys_session(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(RuntimeError, "offline failure"):
                with h.session_root(offline_runtime(), test_env(), Path(tmp)) as s:
                    root = s.root
                    raise RuntimeError("offline failure")
            self.assertFalse(root.exists())

    def test_cleanup_failure_is_not_ignored(self):
        with tempfile.TemporaryDirectory() as tmp:
            captured = None
            try:
                with patch.object(h.shutil, "rmtree", side_effect=OSError("cleanup denied")):
                    with h.session_root(offline_runtime(), test_env(), Path(tmp)) as s:
                        captured = s.root
                self.fail("cleanup should fail")
            except OSError:
                pass
            finally:
                if captured:
                    shutil.rmtree(captured)

    def test_fixture_manifest_rejects_undeclared_test_runtime_and_prompt_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            v, c = h.make_conditions(suite.FIXTURE, Path(tmp) / "conditions", h.copy_fixture)
            (c / "PROJECT_REFERENCE.md").write_text("optional guidance")
            manifest = h.fixture_manifest(v, c, b"same prompt\n", b"same prompt\n")
            differing = [r["path"] for r in manifest["files"] if r["condition_specific"]]
            self.assertEqual(set(differing), h.GUIDANCE)
            for name in ["tests/test_expenses.py", "config.json", "runtime.txt"]:
                target = c / name
                original = target.read_bytes() if target.exists() else None
                target.write_bytes(b"undeclared")
                with self.assertRaisesRegex(h.HarnessError, "undeclared fixture difference"):
                    h.fixture_manifest(v, c, b"same", b"same")
                if original is None:
                    target.unlink()
                else:
                    target.write_bytes(original)
            with self.assertRaisesRegex(h.HarnessError, "prompt bytes"):
                h.fixture_manifest(v, c, b"a", b"b")

    def test_path_escape_and_symlink_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            for name in ["../outside", "/tmp/outside", "."]:
                with self.assertRaises(h.HarnessError):
                    h.local_path(root, name)
            (root / "link").symlink_to(root.parent)
            with self.assertRaises(h.HarnessError):
                h.local_path(root, "link/outside")
            with self.assertRaises(h.HarnessError):
                h.inventory(root)

    def test_real_git_baselines_are_deterministic_and_guidance_only(self):
        runtime = offline_runtime()
        with tempfile.TemporaryDirectory() as tmp:
            baseline = []
            v, c = h.make_conditions(suite.FIXTURE, Path(tmp) / "conditions", h.copy_fixture)
            for source in [v, v, c]:
                with h.session_root(runtime, test_env(), Path(tmp)) as s:
                    s.repo.rmdir()
                    h.copy_fixture(source, s.repo)
                    state = h.initialize_git(s)
                    baseline.append(state)
                    self.assertTrue(state["clean"])
                    self.assertEqual(state["remotes"], "")
                    self.assertEqual(state["hooks"], [])
                    self.assertEqual(state["branch"], "main")
                    self.assertFalse(
                        h.git(s, "diff", "--", "expense_report/report.py", "tests/test_expenses.py")
                    )
            self.assertEqual(baseline[0], baseline[1])
            self.assertEqual(baseline[0]["config"], baseline[2]["config"])
            self.assertNotEqual(baseline[0]["tree"], baseline[2]["tree"])

    def test_environment_and_runtime_drift_fail_receipt_comparison(self):
        runtime = offline_runtime()
        env = test_env()
        self.assertNotIn("PYTHONPATH", h.environment_source("codex", {"PYTHONPATH": "private"}))
        receipt = h.environment_receipt(env, h.Sanitizer().text)
        self.assertEqual(receipt["OPENAI_API_KEY"], {"present": True})
        self.assertNotIn("offline-only-secret", json.dumps(receipt))
        changed = dict(receipt, TZ={"present": True, "value": "different"})
        with self.assertRaisesRegex(h.HarnessError, "environment"):
            h.compare_receipts(receipt, changed, "environment")
        changed = dict(runtime, architecture="different")
        with self.assertRaisesRegex(h.HarnessError, "runtime"):
            h.compare_receipts(runtime, changed, "runtime")

    def test_native_policy_allows_and_denies_the_same_operations(self):
        runtime = offline_runtime()
        with tempfile.TemporaryDirectory() as tmp:
            receipts = []
            for condition in ["vanilla", "contextlean"]:
                with h.session_root(runtime, test_env(), Path(tmp)) as s:
                    try:
                        policy = h.permission_policy(s, "external", "workspace-write")
                        receipt = h.permission_preflight(s, policy, Path(tmp))
                    except h.HarnessError as error:
                        if "Operation not permitted" in str(error) or "no supported native" in str(
                            error
                        ):
                            self.skipTest(
                                "native boundary unavailable in this host/nested sandbox; live preflight fails closed"
                            )
                        raise
                    receipts.append(s.sanitizer.value(receipt))
                    self.assertEqual(
                        receipt["native_preflight"],
                        {
                            "repo_write": True,
                            "tmp_write": True,
                            "parent_write": False,
                            "outside_write": False,
                            "evidence_read": False,
                            "outside_read": False,
                        },
                    )
            h.compare_receipts(*receipts, "permission")
            with self.assertRaisesRegex(h.HarnessError, "permission"):
                h.compare_receipts(
                    receipts[0], dict(receipts[1], sandbox="read-only"), "permission"
                )


class EvidenceTests(unittest.TestCase):
    def test_actual_claude_trace_exposes_four_denials_and_separate_haiku(self):
        path = (
            ROOT
            / "benchmarks/results/2026-10-01-v0.2.1-final/raw/claude-refactor-contextlean/events.jsonl"
        )
        result = trace.parse(path.read_text(), "claude", "<workspace>")
        self.assertEqual(result["commands"], 9)
        self.assertEqual(sum(c["denied"] for c in result["calls"]), 4)
        self.assertEqual(result["usage"]["total_tokens"], 227415)
        self.assertEqual(result["reported_turn_count"], 20)
        self.assertEqual(result["assistant_message_count"], 15)
        self.assertEqual(
            result["auxiliary_model_usage"]["claude-haiku-4-5-20251001"]["inputTokens"], 618
        )
        denied = [c for c in result["calls"] if c["denied"]]
        self.assertTrue(all(c["executed"] is False for c in denied))
        self.assertIn("expansion obfuscation", denied[0]["denial_reason"])

    def test_codex_does_not_invent_stdout_stderr_or_request_usage(self):
        path = (
            ROOT
            / "benchmarks/results/2026-10-01-v0.2.1-final/raw/sol-refactor-contextlean/events.jsonl"
        )
        result = trace.parse(path.read_text(), "codex", "<workspace>")
        calls = [c for c in result["calls"] if c["tool"] == "command_execution"]
        self.assertEqual(len(calls), 5)
        self.assertTrue(all(c["stdout_bytes"] is None and c["stderr_bytes"] is None for c in calls))
        self.assertEqual(result["reported_turn_count"], 1)
        self.assertIsNone(result["assistant_message_count"])
        self.assertEqual(len(result["usage_records"]), 1)
        self.assertEqual(result["verification"][-1]["discovered_count"], 6)
        self.assertIsNone(result["output_byte_totals"]["stdout_bytes"])

    def test_equivalent_coverage_detects_intervening_visible_mutation(self):
        output = "test_a (tests.test_demo.Suite.test_a) ... ok\n\nRan 1 test in 0.01s\n\nOK\n"
        events = []
        for i, command in enumerate(
            [
                "python3 -m unittest tests.test_demo -v",
                "python3 -m unittest discover -s tests -v",
                "python3 -m unittest discover -s tests -v",
            ]
        ):
            if i == 2:
                events.append(
                    {
                        "type": "item.completed",
                        "item": {
                            "id": "edit",
                            "type": "file_change",
                            "changes": [{"path": "test_demo.py"}],
                            "status": "completed",
                        },
                    }
                )
            events.append(
                {
                    "type": "item.completed",
                    "item": {
                        "id": str(i),
                        "type": "command_execution",
                        "command": command,
                        "aggregated_output": output,
                        "exit_code": 0,
                        "status": "completed",
                    },
                }
            )
        parsed = trace.parse("\n".join(map(json.dumps, events)), "codex", "repo")
        checks = parsed["verification"]
        self.assertEqual(checks[1]["equivalent_previous_pass"], 1)
        self.assertFalse(checks[1]["intervening_relevant_change"])
        self.assertTrue(checks[2]["intervening_relevant_change"])
        self.assertIsNone(trace.coverage("pytest", "5 passed")["normalized_test_list_sha256"])

    def test_unavailable_usage_blocks_pair_aggregates_and_interrupt_is_not_task_failure(self):
        interruption = {"success": False, "usage": None, "error": "provider usage limit reached"}
        self.assertEqual(
            h.failure_category(interruption, {"task_success": False}),
            "provider-usage-limit-interruption",
        )
        runs = [
            {
                "task": "refactor",
                "repeat": 1,
                "condition": c,
                "metrics": {"total_tokens": 100 if c == "vanilla" else None},
            }
            for c in ["vanilla", "contextlean"]
        ]
        self.assertIsNone(h.paired_metrics(runs, ["refactor"], 1)[0]["differences"]["total_tokens"])
        self.assertIsNone(
            trace.normalize_usage(
                {"input_tokens": True, "cached_input_tokens": 0, "output_tokens": 1}
            )
        )
        self.assertIsNone(
            trace.normalize_usage({"input_tokens": 2, "cached_input_tokens": 3, "output_tokens": 1})
        )

    def test_saved_schedule_counterbalances_before_results_exist(self):
        plan = h.schedule(["refactor"], 3)
        self.assertEqual(
            [p["condition"] for p in plan],
            ["vanilla", "contextlean", "contextlean", "vanilla", "vanilla", "contextlean"],
        )
        stats = h.distribution([1, 3, 8])
        self.assertEqual(stats["observations"], [1, 3, 8])
        self.assertEqual(stats["median"], 3)
        self.assertIsNotNone(stats["sample_standard_deviation"])

    def test_public_sanitization_removes_paths_secrets_and_account_identifiers(self):
        s = h.Sanitizer(Path("/private/tmp/session-A"), secrets=["opaque-secret-123"])
        value = s.value(
            {
                "command": "cat /private/tmp/session-A/repo/a /Users/andy/private opaque-secret-123",
                "account_id": "acct-private",
                "organization_id": "org-private",
                "userId": "user-private",
                "accessToken": "opaque-secret-123",
                "env": {"OPENAI_API_KEY": {"present": True}},
                "outside": "/private/tmp/unrecognized/secret",
            }
        )
        text = json.dumps(value)
        for prohibited in [
            "/Users/andy",
            "/private/tmp",
            "opaque-secret-123",
            "acct-private",
            "org-private",
            "user-private",
        ]:
            self.assertNotIn(prohibited, text)
        self.assertIn("<session-root>/repo/a", text)
        self.assertEqual(value["env"]["OPENAI_API_KEY"], {"present": True})

    def test_private_stream_is_byte_exact_without_a_provider_launch(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            with h.session_root(offline_runtime(), test_env(), output) as session:
                # Only the pinned Python interpreter executes this literal print.
                command = [
                    sys.executable,
                    "-c",
                    "import sys;sys.stdout.buffer.write(b'raw\\r\\n');sys.stderr.buffer.write(b'err\\r\\n')",
                ]
                with patch.object(h, "execution_command", side_effect=lambda s, p, c, o: c):
                    result = h.execute_session(
                        session, command, "", 10, {"native_preflight": True}, output
                    )
                private = output / "private" / session.root.name
                self.assertEqual((private / "events.jsonl").read_bytes(), b"raw\r\n")
                self.assertEqual((private / "events.stderr.txt").read_bytes(), b"err\r\n")
                self.assertEqual(result["stdout_bytes"], 5)
                self.assertEqual((private / "events.jsonl").stat().st_mode & 0o777, 0o600)

    def test_stream_reports_and_unclassified_model_usage_are_not_dropped_or_summed(self):
        message = {
            "type": "assistant",
            "message": {
                "id": "same",
                "usage": {
                    "input_tokens": 2,
                    "output_tokens": 1,
                    "cache_creation_input_tokens": 0,
                    "cache_read_input_tokens": 0,
                },
            },
        }
        events = [
            message,
            message,
            {"type": "result", "modelUsage": {"unknown-model": {"inputTokens": 9}}},
        ]
        parsed = trace.parse("\n".join(map(json.dumps, events)), "claude", "repo")
        self.assertEqual(len(parsed["usage_records"]), 2)
        self.assertEqual(parsed["assistant_message_count"], 1)
        self.assertEqual(parsed["auxiliary_model_usage"], {})
        self.assertIn("unknown-model", parsed["unclassified_model_usage"])


class RunnerGateTests(unittest.TestCase):
    def test_effective_runtime_mismatch_prevents_any_model_launch(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            prepare_receipt(tmp / "preparation.json")
            args = args_for(tmp)
            runtime = offline_runtime()
            runtime["binaries"]["python3"]["version"] = "Python deliberately mismatched"
            with (
                patch.object(h, "pin_runtime", return_value=runtime),
                patch.object(h, "environment_source", return_value=test_env()),
                patch.object(h, "permission_preflight", side_effect=fake_permission),
                patch.object(h, "permission_policy", return_value={"sandbox": "workspace-write"}),
                patch.object(h, "boundary_command", side_effect=lambda s, p, c, o: c),
                patch.object(h, "execute_session") as launch,
            ):
                with self.assertRaisesRegex(h.HarnessError, "effective python3 mismatch"):
                    suite.run(args)
            launch.assert_not_called()
            report = json.loads((args.output_dir / "summary.json").read_text())
            self.assertEqual(report["model_calls"], 0)
            self.assertEqual(report["status"], "harness-preparation-failure")
            self.assertTrue(report["preparation_slots"][0]["cleanup_verified"])

    def test_deterministic_preparation_failure_prevents_any_launch(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            prepare_receipt(tmp / "preparation.json")
            args = args_for(tmp)
            with (
                patch.object(h, "pin_runtime", return_value=offline_runtime()),
                patch.object(h, "environment_source", return_value=test_env()),
                patch.object(
                    h, "permission_preflight", side_effect=h.HarnessError("offline policy failure")
                ),
                patch.object(h, "execute_session") as launch,
            ):
                with self.assertRaisesRegex(h.HarnessError, "offline policy failure"):
                    suite.run(args)
            launch.assert_not_called()
            report = json.loads((args.output_dir / "summary.json").read_text())
            self.assertEqual(report["model_calls"], 0)
            self.assertEqual(report["status"], "harness-preparation-failure")
            self.assertTrue((args.output_dir / "schedule.json").exists())

    def test_interruption_is_retained_without_retry_or_invalid_aggregate(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            prepare_receipt(tmp / "preparation.json")
            args = args_for(tmp)
            with (
                patch.object(h, "pin_runtime", return_value=offline_runtime()),
                patch.object(h, "environment_source", return_value=test_env()),
                patch.object(h, "permission_preflight", side_effect=fake_permission),
                patch.object(
                    h, "effective_runtime_preflight", return_value={"passed": True, "mocked": True}
                ),
                patch.object(h, "permission_policy", return_value={"sandbox": "read-only"}),
                patch.object(h, "boundary_command", side_effect=lambda s, p, c, o: c),
                patch.object(
                    h,
                    "execute_session",
                    return_value={
                        "stdout": json.dumps(
                            {
                                "type": "turn.failed",
                                "error": {"message": "provider usage limit reached"},
                            }
                        ),
                        "stderr": "",
                        "exit_code": 1,
                        "error": None,
                        "duration_seconds": 1,
                    },
                ) as launch,
            ):
                report = suite.run(args)
            self.assertEqual(launch.call_count, 1)
            self.assertEqual(report["status"], "incomplete")
            run = report["runs"][0]
            self.assertEqual(run["failure_category"], "provider-usage-limit-interruption")
            self.assertIsNone(run["evaluation"]["task_success"])
            self.assertTrue(run["cleanup_verified"])
            self.assertIsNone(report["paired_differences"][0]["differences"]["total_tokens"])
            self.assertEqual(report["summary"][0]["vanilla"]["task_failures"], 0)
            self.assertEqual(report["model_calls"], 1)
            for file in args.output_dir.rglob("*"):
                if file.is_file() and "private" not in file.relative_to(args.output_dir).parts:
                    content = file.read_text()
                    self.assertNotIn("/Users/andy/", content)
                    self.assertNotIn("offline-only-secret", content)
                    self.assertNotIn(str(tmp), content)
            checksums = json.loads((args.output_dir / "checksums.json").read_text())
            self.assertTrue(
                all(
                    h.digest((args.output_dir / name).read_bytes()) == value
                    for name, value in checksums.items()
                )
            )
            self.assertTrue(
                (args.output_dir / "private/navigation-1-vanilla/session.json").exists()
            )

    def test_performance_minimum_and_preflight_only_never_launch(self):
        with tempfile.TemporaryDirectory() as tmp:
            args = args_for(Path(tmp), experiment_kind="performance", repeat=2)
            with patch.object(h, "execute_session") as launch:
                with self.assertRaisesRegex(suite.core.BenchmarkError, "at least 3"):
                    suite.run(args)
                launch.assert_not_called()
            tmp = Path(tmp)
            prepare_receipt(tmp / "preparation.json")
            args = args_for(tmp, live=False, preflight_only=True)
            with (
                patch.object(h, "pin_runtime", return_value=offline_runtime()),
                patch.object(h, "environment_source", return_value=test_env()),
                patch.object(h, "permission_preflight", side_effect=fake_permission),
                patch.object(
                    h, "effective_runtime_preflight", return_value={"passed": True, "mocked": True}
                ),
                patch.object(h, "permission_policy", return_value={"sandbox": "workspace-write"}),
                patch.object(h, "boundary_command", side_effect=lambda s, p, c, o: c),
                patch.object(h, "execute_session") as launch,
            ):
                report = suite.run(args)
            launch.assert_not_called()
            self.assertEqual(report["status"], "preflight-passed")
            self.assertEqual(report["model_calls"], 0)
            self.assertEqual(len(list((args.output_dir / "preflight").glob("*.json"))), 10)


if __name__ == "__main__":
    unittest.main()

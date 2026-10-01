"""Offline validation of the graded suite. Never launches a live model."""

import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("graded_suite", ROOT / "benchmarks/run_benchmark.py")
suite = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(suite)


class SuiteTests(unittest.TestCase):
    def test_five_distinct_categories_and_identical_prompts(self):
        tasks = suite.load_suite(suite.TASKS)
        self.assertEqual(len(tasks), 5)
        self.assertEqual(len({task["category"] for task in tasks}), 5)
        for task in tasks:
            self.assertNotIn("AGENTS.md", suite.task_prompt(task))
            self.assertNotIn("ContextLean", suite.task_prompt(task))

    def test_invalid_duplicate_task_ids_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "tasks.json"
            path.write_text(json.dumps({"tasks": [{"id": "feature", "prompt": "a"}] * 2}))
            with self.assertRaises(suite.core.BenchmarkError):
                suite.load_suite(path)

    def test_fixture_baseline_passes_regression(self):
        passed, _ = suite.capture(
            [suite.sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], suite.FIXTURE
        )
        self.assertTrue(passed)

    def test_repository_copies_exclude_generated_metadata_and_caches(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "source"
            source.mkdir()
            (source / "README.md").write_text("preserve source documentation")
            (source / ".DS_Store").write_bytes(b"generated metadata")
            (source / ".ruff_cache").mkdir()
            (source / ".ruff_cache/data").write_bytes(b"generated cache")
            destination = Path(tmp) / "copy"
            suite.core.copy_repository(source, destination)
            self.assertEqual([path.name for path in destination.iterdir()], ["README.md"])

    def test_unmodified_fixture_fails_every_edit_acceptance(self):
        for task in suite.load_suite(suite.TASKS)[1:]:
            with self.subTest(task=task["id"]), tempfile.TemporaryDirectory() as tmp:
                work = Path(tmp) / "repo"
                suite.core.copy_repository(suite.FIXTURE, work)
                result = suite.grade(task, work, {"success": True}, Path(tmp) / "raw")
                self.assertTrue(result["tests_passed"])
                self.assertFalse(result["task_success"])

    def test_known_correct_solutions_pass_acceptance(self):
        for task in suite.load_suite(suite.TASKS):
            with self.subTest(task=task["id"]), tempfile.TemporaryDirectory() as tmp:
                work = Path(tmp) / "repo"
                suite.core.copy_repository(suite.FIXTURE, work)
                response = ""
                if task["id"] == "navigation":
                    response = json.dumps(
                        {
                            "loader": "expense_report/storage.py",
                            "reporter": "expense_report/report.py",
                            "cli_tests": "tests/test_expenses.py",
                            "total": "40.00",
                            "count": 3,
                            "currency": "USD",
                        }
                    )
                elif task["id"] == "bug-fix":
                    path = work / "expense_report/filters.py"
                    path.write_text(
                        path.read_text().replace("== category", "== normalize_category(category)")
                    )
                elif task["id"] == "feature":
                    path = work / "expense_report/cli.py"
                    text = path.read_text().replace(
                        'parser.add_argument("--category")',
                        'parser.add_argument("--category")\n    parser.add_argument("--min-amount")',
                    )
                    text = text.replace(
                        "print(json.dumps(",
                        'if args.min_amount is not None:\n        from decimal import Decimal\n        expenses = [item for item in expenses if item["amount"] >= Decimal(args.min_amount)]\n    print(json.dumps(',
                    )
                    path.write_text(text)
                elif task["id"] == "refactor":
                    path = work / "expense_report/report.py"
                    path.write_text(
                        path.read_text().replace(
                            "def normalize_category(value):\n    return value.strip().casefold()",
                            "from expense_report.filters import normalize_category",
                        )
                    )
                else:
                    (work / "config.json").write_text('{"currency": "EUR"}\n')
                    path = work / "README.md"
                    path.write_text(path.read_text().replace("USD", "EUR"))
                result = suite.grade(
                    task, work, {"success": True, "final_response": response}, Path(tmp) / "raw"
                )
                self.assertTrue(result["task_success"])

    def test_deleted_regression_tests_cannot_hide_broken_behavior(self):
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp) / "repo"
            suite.core.copy_repository(suite.FIXTURE, work)
            shutil.rmtree(work / "tests")
            (work / "expense_report/report.py").write_text(
                "def build_report(*args):\n    return {}\n"
            )
            result = suite.grade({"id": "bug-fix"}, work, {"success": True}, Path(tmp) / "raw")
            self.assertFalse(result["tests_passed"])
            self.assertFalse(result["task_success"])

    def test_missing_optional_reasoning_does_not_fail_usage(self):
        result = suite.core.parse_jsonl(
            '{"type":"turn.completed","usage":{"input_tokens":5,"cached_input_tokens":0,"output_tokens":2}}'
        )
        self.assertTrue(result["success"])
        self.assertIsNone(result["usage"]["reasoning_output_tokens"])
        usage = dict(result, duration_seconds=1)
        self.assertIsNone(suite.core.aggregate_runs([usage])["reasoning_output_tokens"])

    def test_boolean_usage_is_rejected(self):
        result = suite.core.parse_jsonl(
            '{"type":"turn.completed","usage":{"input_tokens":true,"cached_input_tokens":0,"output_tokens":2}}'
        )
        self.assertFalse(result["success"])

    def test_failed_runs_remain_in_summary(self):
        runs = [
            {
                "task": "navigation",
                "condition": "vanilla",
                "metrics": {"total_tokens": 100},
                "evaluation": {"task_success": False},
            }
        ]
        summary = suite.summarize(runs, [{"id": "navigation", "category": "navigation"}], 1)[0]
        self.assertEqual(summary["vanilla"]["runs"], 1)
        self.assertEqual(summary["vanilla"]["task_successes"], 0)
        self.assertEqual(summary["vanilla"]["metrics"]["total_tokens"]["median"], 100)

    def test_raw_logs_preserve_events_and_remove_machine_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "events.jsonl"
            suite.core.save_raw_run(
                path, '{"workspace":"/tmp/sample"}', str(Path.home()), Path("/tmp/sample")
            )
            self.assertEqual(json.loads(path.read_text())["workspace"], "<workspace>")
            self.assertEqual(path.with_suffix(".stderr.txt").read_text(), "<home>")

    def test_complete_runner_uses_fresh_equal_starts_and_retains_failures(self):
        starts = []

        def fake_execute(session, command, prompt, timeout, policy, output):
            workspace = session.repo
            starts.append(suite.core.tree_digest(workspace, True))
            self.assertIn("offline-test", command)
            self.assertNotIn("previous-run.txt", [path.name for path in workspace.iterdir()])
            (workspace / "previous-run.txt").write_text("must not reach next run")
            return {
                "stdout": json.dumps(
                    {
                        "type": "turn.completed",
                        "usage": {"input_tokens": 10, "cached_input_tokens": 0, "output_tokens": 2},
                    }
                ),
                "stderr": "",
                "error": None,
                "duration_seconds": 1,
                "exit_code": 0,
            }

        with (
            tempfile.TemporaryDirectory() as tmp,
            patch.object(suite.harness, "execute_session", fake_execute),
            patch.object(
                suite.harness,
                "environment_source",
                return_value=suite.harness.environment_source(
                    "codex", {"OPENAI_API_KEY": "offline-test-secret"}
                ),
            ),
            patch.object(
                suite.harness, "permission_policy", return_value={"sandbox": "workspace-write"}
            ),
            patch.object(
                suite.harness,
                "permission_preflight",
                side_effect=lambda s, p, o: dict(p, native_preflight={"mocked": True}),
            ),
            patch.object(suite.harness, "boundary_command", side_effect=lambda s, p, c, o: c),
        ):
            args = suite.argparse.Namespace(
                model="offline-test",
                reasoning="low",
                repeat=1,
                timeout=10,
                tasks_file=suite.TASKS,
                output_dir=Path(tmp) / "output",
                codex=suite.sys.executable,
                live=True,
                preparation_record=Path(tmp) / "preparation.json",
            )
            # Fake semantic attestation for this mocked runner test only.
            review = {
                "semantics_reviewed": True,
                "entries": {
                    name: {
                        "responsibility": description,
                        "evidence": [
                            {"path": name, "contains": (suite.FIXTURE / name).read_text()}
                        ],
                    }
                    for name, description in suite.preparation.project_map(suite.FIXTURE).items()
                },
            }
            suite.core.write_json(
                args.preparation_record,
                suite.preparation.validate(suite.FIXTURE, review, suite.FIXTURE),
            )
            original_capture = suite.capture

            def capture(command, workspace, timeout=60, **kwargs):
                if command[0] == "unused":
                    return True, "offline fake CLI"
                return original_capture(command, workspace, timeout, **kwargs)

            with patch.object(suite, "capture", capture):
                report = suite.run(args)
            self.assertEqual(len(report["runs"]), 10)
            self.assertEqual(len(set(starts)), 1)
            self.assertIn("No gain claim", report["result"])
            self.assertTrue((args.output_dir / "report.md").is_file())
            self.assertEqual(len(list((args.output_dir / "raw").glob("*/run.json"))), 10)


if __name__ == "__main__":
    unittest.main()

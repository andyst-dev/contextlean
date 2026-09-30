"""Audit the published historical batch offline; never start a model."""

import hashlib
import importlib.util
import json
from pathlib import Path
import stat
import tempfile
import unittest
from unittest.mock import patch
import zipfile


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "benchmarks/results/2026-09-30-validation"
SPEC = importlib.util.spec_from_file_location(
    "published_suite", ROOT / "benchmarks/run_benchmark.py"
)
suite = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(suite)


class PublicValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((DATA / "summary.json").read_text())
        cls.temporary = tempfile.TemporaryDirectory()
        cls.source = Path(cls.temporary.name) / "source"
        cls.solutions = Path(cls.temporary.name) / "solutions"
        for name, destination in [
            ("source-snapshot.zip", cls.source),
            ("solutions.zip", cls.solutions),
        ]:
            with zipfile.ZipFile(DATA / name) as archive:
                for member in archive.infolist():
                    path = Path(member.filename)
                    if path.is_absolute() or ".." in path.parts:
                        raise AssertionError("archive contains an unsafe path")
                    if stat.S_ISLNK(member.external_attr >> 16):
                        raise AssertionError("archive contains a symlink")
                archive.extractall(destination)

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def test_every_raw_artifact_matches_its_checksum(self):
        checksums = json.loads((DATA / "checksums.json").read_text())
        observed = {
            path.relative_to(DATA).as_posix()
            for path in DATA.rglob("*")
            if path.is_file() and path.name not in {"README.md", "checksums.json"}
        }
        self.assertEqual(set(checksums), observed)
        for name, expected in checksums.items():
            with self.subTest(artifact=name):
                self.assertEqual(hashlib.sha256((DATA / name).read_bytes()).hexdigest(), expected)

    def test_frozen_source_and_fair_start_hashes(self):
        fixture = self.source / "benchmarks/fixtures/expense-report"
        selection = json.loads((DATA / "source-selection.json").read_text())
        self.assertEqual(selection["original_candidate_digest"], self.report["candidate_digest"])
        self.assertEqual(
            suite.core.tree_digest(self.source), selection["public_source_tree_digest"]
        )
        files = {
            path.relative_to(self.source).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in self.source.rglob("*")
            if path.is_file()
        }
        self.assertEqual(files, selection["retained_files"])
        self.assertTrue(selection["omitted_generated_files"])
        for name in files:
            self.assertNotIn(".DS_Store", Path(name).parts)
            self.assertNotIn(".ruff_cache", Path(name).parts)
        self.assertEqual(suite.core.tree_digest(fixture), self.report["fixture_digest"])
        for path, field in [
            ("benchmarks/tasks/suite.json", "task_suite_digest"),
            ("benchmarks/evaluate.py", "evaluator_digest"),
        ]:
            self.assertEqual(
                hashlib.sha256((self.source / path).read_bytes()).hexdigest(), self.report[field]
            )
        for run in self.report["runs"]:
            self.assertEqual(
                run["initial_non_instruction_digest"], suite.core.tree_digest(fixture, True)
            )
            self.assertEqual(
                run["initial_digest"],
                suite.core.tree_digest(fixture, run["condition"] == "vanilla"),
            )

    def test_all_ten_usage_records_reconcile_with_raw_events(self):
        self.assertEqual(len(self.report["runs"]), 10)
        self.assertEqual(self.report["repeats"], 1)
        self.assertEqual((self.report["model"], self.report["reasoning"]), ("gpt-5.6-terra", "low"))
        for run in self.report["runs"]:
            with self.subTest(task=run["task"], condition=run["condition"]):
                directory = DATA / run["raw_directory"]
                self.assertEqual(json.loads((directory / "run.json").read_text()), run)
                parsed = suite.core.parse_jsonl((directory / "events.jsonl").read_text())
                self.assertTrue(parsed["success"])
                for key, value in parsed["usage"].items():
                    self.assertEqual(run["metrics"][key], value)
                self.assertEqual(run["metrics"]["command_calls"], parsed["commands"])
                self.assertEqual(
                    run["metrics"]["total_tokens"],
                    parsed["usage"]["input_tokens"] + parsed["usage"]["output_tokens"],
                )
                for key in ("file_reads", "unique_files_inspected", "tool_calls"):
                    self.assertIsNone(run["metrics"][key])

    def test_aggregate_and_both_token_regressions_are_preserved(self):
        expected = {
            "vanilla": (396727, 294400, 6645, 403372, 15, 188.2827120819129),
            "contextlean": (350329, 279296, 4978, 355307, 13, 149.85422099917196),
        }
        keys = (
            "input_tokens",
            "cached_input_tokens",
            "output_tokens",
            "total_tokens",
            "command_calls",
            "duration_seconds",
        )
        for condition, totals in expected.items():
            selected = [run for run in self.report["runs"] if run["condition"] == condition]
            self.assertEqual(len(selected), 5)
            for key, total in zip(keys, totals):
                self.assertAlmostEqual(sum(run["metrics"][key] for run in selected), total)
        for task in ("refactor", "documentation-config"):
            paired = {run["condition"]: run for run in self.report["runs"] if run["task"] == task}
            self.assertGreater(
                paired["contextlean"]["metrics"]["total_tokens"],
                paired["vanilla"]["metrics"]["total_tokens"],
            )
        self.assertEqual(
            suite.summarize(self.report["runs"], self.report["tasks"], 1), self.report["summary"]
        )

    def test_saved_solutions_still_pass_the_frozen_evaluator(self):
        fixture = self.source / "benchmarks/fixtures/expense-report"
        with (
            patch.object(suite, "ROOT", self.source),
            patch.object(suite, "FIXTURE", fixture),
            patch.object(
                suite.core, "execute_run", side_effect=AssertionError("live run forbidden")
            ),
        ):
            for run in self.report["runs"]:
                with self.subTest(task=run["task"], condition=run["condition"]):
                    parsed = suite.core.parse_jsonl(
                        (DATA / run["raw_directory"] / "events.jsonl").read_text()
                    )
                    solution = self.solutions / Path(run["raw_directory"]).name / "solution"
                    result = suite.grade(
                        {"id": run["task"]},
                        solution,
                        parsed,
                        Path(self.temporary.name) / "evaluation" / str(run["sequence"]),
                    )
                    self.assertEqual(result, run["evaluation"])
                    self.assertEqual(
                        (solution / "data/sample.csv").read_bytes(),
                        (fixture / "data/sample.csv").read_bytes(),
                    )
                    for name in ("AGENTS.md", "CLAUDE.md"):
                        if run["condition"] == "contextlean":
                            self.assertEqual(
                                (solution / name).read_bytes(), (fixture / name).read_bytes()
                            )
                        else:
                            self.assertFalse((solution / name).exists())
                    if run["task"] == "navigation":
                        self.assertEqual(suite.core.tree_digest(solution), run["initial_digest"])


if __name__ == "__main__":
    unittest.main()

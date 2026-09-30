"""Reconcile the final candidate diagnostic batch offline; never invoke a model."""

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
DATA = ROOT / "benchmarks/results/2026-09-30-final-0.2.0"
SPEC = importlib.util.spec_from_file_location("final_suite", ROOT / "benchmarks/run_benchmark.py")
suite = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(suite)


class FinalValidationTests(unittest.TestCase):
    data = DATA

    def test_artifacts_and_raw_measurements(self):
        report = json.loads((self.data / "summary.json").read_text())
        self.assertEqual(len(report["runs"]), 10)
        self.assertEqual(report["git_commit"], "52a2c34c091f9720076cc9685fb858347d9f6dcf")
        previous = json.loads(
            (ROOT / "benchmarks/results/2026-09-30-validation/summary.json").read_text()
        )
        for key in ("tasks", "configuration", "environment", "model", "reasoning", "repeats"):
            self.assertEqual(report[key], previous[key])
        checksums = json.loads((self.data / "checksums.json").read_text())
        observed = {
            p.relative_to(self.data).as_posix()
            for p in self.data.rglob("*")
            if p.is_file() and p.name not in {"README.md", "checksums.json"}
        }
        self.assertEqual(observed, set(checksums))
        for name, digest in checksums.items():
            self.assertEqual(hashlib.sha256((self.data / name).read_bytes()).hexdigest(), digest)
        for run in report["runs"]:
            directory = self.data / run["raw_directory"]
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
            for key in ("file_reads", "tool_calls", "unique_files_inspected"):
                self.assertIsNone(run["metrics"][key])

    def test_frozen_solutions_regrade_and_fair_start(self):
        report = json.loads((self.data / "summary.json").read_text())
        with tempfile.TemporaryDirectory() as temporary:
            source, solutions = Path(temporary) / "source", Path(temporary) / "solutions"
            for name, destination in (
                ("source-snapshot.zip", source),
                ("solutions.zip", solutions),
            ):
                with zipfile.ZipFile(self.data / name) as archive:
                    for member in archive.infolist():
                        path = Path(member.filename)
                        self.assertFalse(path.is_absolute())
                        self.assertNotIn("..", path.parts)
                        self.assertFalse(stat.S_ISLNK(member.external_attr >> 16))
                    archive.extractall(destination)
            self.assertEqual(suite.core.tree_digest(source), report["candidate_digest"])
            fixture = source / "benchmarks/fixtures/expense-report"
            self.assertEqual(suite.core.tree_digest(fixture), report["fixture_digest"])
            with (
                patch.object(suite, "ROOT", source),
                patch.object(suite, "FIXTURE", fixture),
                patch.object(
                    suite.core, "execute_run", side_effect=AssertionError("live forbidden")
                ),
            ):
                for run in report["runs"]:
                    directory = self.data / run["raw_directory"]
                    parsed = suite.core.parse_jsonl((directory / "events.jsonl").read_text())
                    solution = solutions / Path(run["raw_directory"]).name / "solution"
                    self.assertEqual(
                        run["initial_digest"],
                        suite.core.tree_digest(fixture, run["condition"] == "vanilla"),
                    )
                    self.assertEqual(
                        run["initial_non_instruction_digest"], suite.core.tree_digest(fixture, True)
                    )
                    graded = suite.grade(
                        {"id": run["task"]},
                        solution,
                        parsed,
                        Path(temporary) / "regrade" / str(run["sequence"]),
                    )
                    self.assertEqual(graded, run["evaluation"])
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

    def test_aggregate_cost_and_quality_limitation(self):
        report = json.loads((self.data / "summary.json").read_text())
        review = json.loads((self.data / "measurement-review.json").read_text())
        for condition, aggregate in review["aggregate"].items():
            runs = [r for r in report["runs"] if r["condition"] == condition]
            for key in (
                "input_tokens",
                "cached_input_tokens",
                "output_tokens",
                "total_tokens",
                "command_calls",
                "duration_seconds",
            ):
                self.assertAlmostEqual(aggregate[key], sum(r["metrics"][key] for r in runs))
        rate = suite.core.find_rate(review["rate_card"], report["model"])
        self.assertAlmostEqual(
            review["total_standard_credit_equivalent"],
            sum(suite.core.calculate_credits(r["metrics"], rate) for r in report["runs"]),
        )
        self.assertFalse(review["headline_eligible"])
        self.assertIn("expense_report/config.json", review["bootstrap_quality_warning"])
        self.assertIsNone(review["actual_credits_spent"])
        self.assertEqual(len(review["regrading"]), 10)
        self.assertEqual(review["additional_runs"], 0)

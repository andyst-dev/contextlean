"""Offline fail-fast preparation contracts; no real model or CLI calls."""

import argparse
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "preflight_suite", ROOT / "benchmarks/run_benchmark.py"
)
suite = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(suite)
prep = suite.preparation


def fake_review(repo):
    """Synthetic review for checker tests, not an actual ownership attestation."""
    return {
        "semantics_reviewed": True,
        "entries": {
            name: {
                "responsibility": description,
                "evidence": [{"path": name, "contains": (repo / name).read_text()}],
            }
            for name, description in prep.project_map(repo).items()
        },
    }


class PreparationTests(unittest.TestCase):
    def test_nonexistent_map_path_rejects_freeze_and_live_runner_before_calls(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo, frozen, receipt = (Path(tmp) / n for n in ("prepared", "frozen", "record.json"))
            suite.core.copy_repository(suite.FIXTURE, repo)
            review = fake_review(repo)
            suite.core.write_json(receipt, prep.validate(repo, review, suite.FIXTURE))
            path = repo / "AGENTS.md"
            path.write_text(
                path.read_text().replace("`config.json`", "`expense_report/config.json`")
            )
            with self.assertRaisesRegex(suite.core.BenchmarkError, "nonexistent mapped path"):
                prep.freeze(suite.FIXTURE, repo, review, frozen, Path(tmp) / "new-record.json")
            self.assertFalse(frozen.exists())
            args = argparse.Namespace(
                tasks_file=suite.TASKS,
                repeat=1,
                timeout=10,
                output_dir=Path(tmp) / "results",
                preparation_record=receipt,
            )
            # Preparation imports the same exception definition from its core instance.
            with (
                patch.object(suite, "FIXTURE", repo),
                patch.object(suite, "capture") as cli,
                patch.object(suite.core, "execute_run") as live,
                self.assertRaisesRegex(prep.core.BenchmarkError, "nonexistent mapped path"),
            ):
                suite.run(args)
            cli.assert_not_called()
            live.assert_not_called()
            self.assertFalse(args.output_dir.exists())

    def test_review_is_required_and_bound_to_responsibility_and_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "prepared"
            suite.core.copy_repository(suite.FIXTURE, repo)
            with self.assertRaisesRegex(prep.core.BenchmarkError, "explicit source review"):
                prep.validate(repo, {})
            review = fake_review(repo)
            review["entries"]["config.json"]["responsibility"] = "CSV loading"
            with self.assertRaisesRegex(prep.core.BenchmarkError, "changed responsibility"):
                prep.validate(repo, review)
            review = fake_review(repo)
            review["entries"]["config.json"]["evidence"][0]["contains"] = "def load_csv"
            with self.assertRaisesRegex(prep.core.BenchmarkError, "evidence not found"):
                prep.validate(repo, review)

    def test_non_guidance_change_and_stale_frozen_context_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo, frozen, receipt = (Path(tmp) / n for n in ("prepared", "frozen", "record.json"))
            suite.core.copy_repository(suite.FIXTURE, repo)
            review = fake_review(repo)
            prep.freeze(suite.FIXTURE, repo, review, frozen, receipt)
            self.assertEqual(
                prep.validate_frozen(frozen, receipt)["vanilla_digest"],
                suite.core.tree_digest(suite.FIXTURE, True),
            )
            path = frozen / "AGENTS.md"
            path.write_text(path.read_text() + "\nChanged after freeze.\n")
            with self.assertRaisesRegex(prep.core.BenchmarkError, "has changed"):
                prep.validate_frozen(frozen, receipt)
            path = repo / "config.json"
            path.write_text('{"currency": "EUR"}\n')
            with self.assertRaisesRegex(prep.core.BenchmarkError, "outside agent guidance"):
                prep.validate(repo, fake_review(repo), suite.FIXTURE)

    def test_missing_receipt_and_unsupported_paths_fail_closed(self):
        with self.assertRaisesRegex(prep.core.BenchmarkError, "record required"):
            prep.validate_frozen(suite.FIXTURE, None)
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "prepared"
            suite.core.copy_repository(suite.FIXTURE, repo)
            path = repo / "AGENTS.md"
            text = path.read_text()
            for name in ("../config.json", "/config.json"):
                path.write_text(text.replace("`config.json`", f"`{name}`"))
                with self.assertRaisesRegex(prep.core.BenchmarkError, "inside the fixture"):
                    prep.project_map(repo)
            path.write_text(text.replace("`config.json`:", "`config.json`"))
            with self.assertRaisesRegex(prep.core.BenchmarkError, "unparsed path"):
                prep.project_map(repo)

    def test_refreshed_receipt_cannot_change_context_mid_batch(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo, frozen, receipt = (Path(tmp) / n for n in ("prepared", "frozen", "record.json"))
            suite.core.copy_repository(suite.FIXTURE, repo)
            review = fake_review(repo)
            original = prep.freeze(suite.FIXTURE, repo, review, frozen, receipt)
            path = frozen / "AGENTS.md"
            path.write_text(path.read_text() + "\nNew guidance after batch start.\n")
            suite.core.write_json(receipt, prep.validate(frozen, review))
            with self.assertRaisesRegex(prep.core.BenchmarkError, "changed during the batch"):
                prep.validate_frozen(frozen, receipt, original)

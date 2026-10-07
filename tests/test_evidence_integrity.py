"""Published ledgers and Balanced outcomes are checked without model execution."""

import io
import json
from pathlib import Path
import stat
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from evidence_support import assert_checksums, assert_usage, extract_archive, load_frozen_module


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "benchmarks/results"


class PublishedIntegrityTests(unittest.TestCase):
    def test_all_published_checksum_ledgers(self):
        ledgers = sorted(RESULTS.rglob("checksums.json"))
        self.assertTrue(ledgers)
        for ledger in ledgers:
            assert_checksums(self, ledger)

    def test_archive_extraction_rejects_escape_and_symlink_before_writing(self):
        for name, mode in [("../escape", 0), ("/absolute", 0), ("link", stat.S_IFLNK)]:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as temporary:
                data = io.BytesIO()
                with zipfile.ZipFile(data, "w") as archive:
                    archive.writestr("safe", "must not be written before validation")
                    member = zipfile.ZipInfo(name)
                    member.external_attr = mode << 16
                    archive.writestr(member, "outside")
                data.seek(0)
                destination = Path(temporary) / "extracted"
                with self.assertRaises(AssertionError):
                    extract_archive(data, destination)
                self.assertFalse(destination.exists())


class BalancedPublicationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.campaign = RESULTS / "2026-10-06-balanced-product-change/campaign"
        cls.report = json.loads((cls.campaign / "summary.json").read_text())
        # Public source is sanitized and may be non-executable. Regrade with the
        # current offline orchestration and the frozen evaluator/original tests.
        cls.runner = load_frozen_module(
            "balanced_evidence_reader", ROOT / "benchmarks/run_benchmark.py"
        )

    def test_frozen_usage_identity_and_summary_reconcile(self):
        self.assertEqual(len(self.report["runs"]), 6)
        self.assertEqual(self.report["conditions"], ["old", "balanced"])
        revisions = {
            "old": "ae8653b123bdb4c686ee36825c80db851c8595ea",
            "balanced": "1a6e67fb9e5c3d5a91ca89a9f5466d2fa037ea52",
        }
        for run in self.report["runs"]:
            with self.subTest(sequence=run["sequence"]):
                directory = self.campaign / run["raw_directory"]
                self.assertEqual(json.loads((directory / "run.json").read_text()), run)
                parsed = self.runner.core.parse_jsonl((directory / "events.jsonl").read_text())
                assert_usage(self, run, parsed)
                self.assertEqual(run["product_revision"], revisions[run["condition"]])
                self.assertEqual(run["condition_kind"], "guided_product_revision")
                self.assertTrue(run["cleanup_verified"])
                self.assertTrue(run["measurement_complete"])
        labels = {"old": "vanilla", "balanced": "contextlean"}
        runs = [dict(run, condition=labels[run["condition"]]) for run in self.report["runs"]]
        expected = [
            {labels.get(key, key): value for key, value in task.items()}
            for task in self.report["summary"]
        ]
        self.assertEqual(self.runner.summarize(runs, self.report["tasks"], 3), expected)

    def test_all_six_saved_solutions_pass_frozen_grading(self):
        runner = self.runner
        with (
            tempfile.TemporaryDirectory() as temporary,
            patch.object(runner, "ROOT", self.campaign / "source"),
            patch.object(runner.core, "execute_run", side_effect=AssertionError("live forbidden")),
            patch.object(
                runner.harness, "execute_session", side_effect=AssertionError("live forbidden")
            ),
        ):
            for run in self.report["runs"]:
                with (
                    self.subTest(sequence=run["sequence"]),
                    patch.object(runner, "FIXTURE", self.campaign / "fixtures" / run["condition"]),
                ):
                    directory = self.campaign / run["raw_directory"]
                    parsed = runner.core.parse_jsonl((directory / "events.jsonl").read_text())
                    result = runner.grade(
                        {"id": run["task"]},
                        directory / "solution",
                        parsed,
                        Path(temporary) / str(run["sequence"]),
                    )
                    self.assertEqual(result, run["evaluation"])
                    self.assertTrue(all(result.values()))

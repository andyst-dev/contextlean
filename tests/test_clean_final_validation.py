"""Offline contracts for the fresh final batch; no model execution."""

import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import zipfile

import test_final_validation as diagnostic

suite = diagnostic.suite


ROOT = Path(__file__).resolve().parents[1]


class CleanFinalValidationTests(diagnostic.FinalValidationTests):
    data = ROOT / "benchmarks/results/2026-09-30-clean-final-0.2.0"

    def test_aggregate_cost_and_quality_limitation(self):
        report = json.loads((self.data / "summary.json").read_text())
        review = json.loads((self.data / "measurement-review.json").read_text())
        for condition, aggregate in review["aggregate"].items():
            runs = [r for r in report["runs"] if r["condition"] == condition]
            for key, value in aggregate.items():
                self.assertAlmostEqual(value, sum(r["metrics"][key] for r in runs))
        rate = suite.core.find_rate(review["rate_card"], report["model"])
        self.assertAlmostEqual(
            review["total_standard_credit_equivalent"],
            sum(suite.core.calculate_credits(r["metrics"], rate) for r in report["runs"]),
        )
        self.assertTrue(review["headline_eligible"])
        self.assertIsNone(review["actual_credits_spent"])
        self.assertEqual(len(review["regrading"]), 10)
        self.assertEqual(review["additional_runs"], 0)
        for task in report["tasks"]:
            pair = {r["condition"]: r for r in report["runs"] if r["task"] == task["id"]}
            expected = [
                key
                for key in ("total_tokens", "duration_seconds", "command_calls")
                if pair["contextlean"]["metrics"][key] > pair["vanilla"]["metrics"][key]
            ]
            self.assertEqual(review["negative_cases"][task["id"]], expected)

    def test_all_preparations_remain_current_and_complete(self):
        evidence = json.loads((self.data / "preparation-evidence.json").read_text())
        self.assertEqual(evidence["status"], "PASS")
        self.assertFalse(evidence["previous_generated_guidance_reused"])
        self.assertEqual(evidence["model_calls_before_preflight"], 0)
        self.assertEqual(len(evidence["tasks"]), 5)
        self.assertEqual(evidence["product_commit"], "52a2c34c091f9720076cc9685fb858347d9f6dcf")
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "source"
            with zipfile.ZipFile(self.data / "source-snapshot.zip") as archive:
                archive.extractall(source)
            fixture = source / "benchmarks/fixtures/expense-report"
            receipt = json.loads((self.data / "preparation.json").read_text())
            self.assertEqual(suite.preparation.validate(fixture, receipt["review"]), receipt)
            spec = importlib.util.spec_from_file_location(
                "frozen_transfer", source / "skills/bootstrap/scripts/verify_transfer.py"
            )
            transfer = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(transfer)
            report = json.loads((self.data / "summary.json").read_text())
            self.assertLessEqual(evidence["prepared_at"], report["started_at"])
            for task in evidence["tasks"]:
                self.assertEqual(task["record"], receipt)
                self.assertEqual(task["transfer_check"]["facets"], 71)
                self.assertTrue(task["safe_removal_verified"])
                self.assertEqual(
                    transfer.verify(fixture, task["transfer"], source), task["transfer_check"]
                )
            for path, digest in evidence["protected_hashes"].items():
                self.assertEqual(hashlib.sha256((source / path).read_bytes()).hexdigest(), digest)

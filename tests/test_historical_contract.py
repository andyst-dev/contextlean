"""Historical contract and preservation checks; never current Bootstrap gates."""

from collections import Counter
import importlib.util
import json
from pathlib import Path
import re
import unittest

from evidence_support import fingerprint


ROOT = Path(__file__).resolve().parents[1]


class HistoricalComparisonTests(unittest.TestCase):
    def test_balanced_comparison_does_not_relabel_retirements_as_pass(self):
        text = (ROOT / "docs/history/2026-10-05-balanced-migration.md").read_text()
        statuses = re.findall(r"^\| \d+ \|.*?\| (PASS|RE-SCOPED|RETIRED|REPLACED) \|", text, re.M)
        self.assertEqual(
            Counter(statuses), {"PASS": 55, "RE-SCOPED": 13, "RETIRED": 6, "REPLACED": 2}
        )
        self.assertIn("intentional product simplification", text.lower())
        self.assertIn("semantic regression", text)

    def test_legacy_receipt_remains_explicitly_inspectable(self):
        spec = importlib.util.spec_from_file_location(
            "legacy_transfer", ROOT / "tests/legacy_bootstrap.py"
        )
        legacy = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(legacy)
        fixture = ROOT / "tests/fixtures/bootstrap-transfer"
        result = legacy.verify(fixture, json.loads((fixture / "transfer.json").read_text()))
        self.assertFalse(result["setup_specification_required"])

    def test_historical_evidence_and_original_reference_are_unchanged(self):
        expected = json.loads(
            (ROOT / "tests/fixtures/bootstrap-core/historical-hashes.json").read_text()
        )
        for relative, digest in expected.items():
            with self.subTest(path=relative):
                self.assertEqual(fingerprint(ROOT / relative), digest)

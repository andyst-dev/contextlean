from decimal import Decimal
import json
import subprocess
import sys
import unittest

from expense_report.filters import select_category
from expense_report.report import build_report
from expense_report.storage import load_expenses


class ExpenseTests(unittest.TestCase):
    def test_load_decimal(self):
        rows = load_expenses("data/sample.csv")
        self.assertEqual(rows[0]["amount"], Decimal("12.50"))

    def test_filter(self):
        rows = load_expenses("data/sample.csv")
        self.assertEqual(len(select_category(rows, "food")), 2)
        self.assertEqual(len(select_category(rows, None)), 3)

    def test_report(self):
        report = build_report(load_expenses("data/sample.csv"), "GBP")
        self.assertEqual(report["total"], "40.00")
        self.assertEqual(report["categories"], {"food": "20.00", "travel": "20.00"})
        self.assertEqual(report["currency"], "GBP")

    def test_cli_override(self):
        result = subprocess.run(
            [sys.executable, "-m", "expense_report.cli", "data/sample.csv", "--currency", "GBP"],
            capture_output=True, text=True, check=True,
        )
        self.assertEqual(json.loads(result.stdout)["currency"], "GBP")

    def test_configured_default(self):
        result = subprocess.run(
            [sys.executable, "-m", "expense_report.cli", "data/sample.csv"],
            capture_output=True, text=True, check=True,
        )
        self.assertEqual(json.loads(result.stdout)["currency"], "EUR")

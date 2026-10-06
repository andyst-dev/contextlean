from decimal import Decimal
import json
from pathlib import Path
import subprocess
import sys
import unittest

from expense_report.filters import select_category, select_min_amount
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

    def test_min_amount_filter(self):
        rows = load_expenses("data/sample.csv")
        self.assertEqual(
            [row["amount"] for row in select_min_amount(rows, Decimal("10"))],
            [Decimal("12.50"), Decimal("20.00")],
        )
        self.assertEqual(select_min_amount(rows, None), rows)

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
        self.assertEqual(json.loads(result.stdout)["currency"], json.loads(Path("config.json").read_text())["currency"])

    def test_cli_min_amount(self):
        result = subprocess.run(
            [sys.executable, "-m", "expense_report.cli", "data/sample.csv", "--min-amount", "10"],
            capture_output=True, text=True, check=True,
        )
        report = json.loads(result.stdout)
        self.assertEqual(report["count"], 2)
        self.assertEqual(report["total"], "32.50")

    def test_cli_category_and_min_amount(self):
        result = subprocess.run(
            [
                sys.executable, "-m", "expense_report.cli", "data/sample.csv",
                "--category", "food", "--min-amount", "10",
            ],
            capture_output=True, text=True, check=True,
        )
        report = json.loads(result.stdout)
        self.assertEqual(report["count"], 1)
        self.assertEqual(report["total"], "12.50")

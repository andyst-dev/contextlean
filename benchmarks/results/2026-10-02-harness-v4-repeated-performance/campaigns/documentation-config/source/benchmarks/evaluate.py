"""Independent acceptance checks, run outside the agent's measured conversation."""

import ast
import json
from pathlib import Path
import subprocess
import sys
import unittest
from decimal import Decimal


def evaluate(task, workspace, response):
    sys.path.insert(0, str(workspace))
    from expense_report.filters import select_category
    from expense_report.report import build_report
    from expense_report.storage import load_expenses

    def cli(*args):
        result = subprocess.run(
            [sys.executable, "-m", "expense_report.cli", "data/sample.csv", *args],
            cwd=workspace,
            capture_output=True,
            text=True,
            timeout=20,
            check=True,
        )
        return json.loads(result.stdout)

    class Acceptance(unittest.TestCase):
        def test_task_contract(self):
            rows = load_expenses(workspace / "data/sample.csv")
            if task == "navigation":
                answer = response.strip()
                if answer.startswith("```json") and answer.endswith("```"):
                    answer = answer[7:-3].strip()
                self.assertEqual(
                    json.loads(answer),
                    {
                        "loader": "expense_report/storage.py",
                        "reporter": "expense_report/report.py",
                        "cli_tests": "tests/test_expenses.py",
                        "total": "40.00",
                        "count": 3,
                        "currency": "USD",
                    },
                )
            elif task == "bug-fix":
                for query in (" FOOD ", "Food", "food", "fOoD"):
                    result = cli("--category", query)
                    self.assertEqual(result["count"], 2)
                    self.assertEqual(Decimal(result["total"]), Decimal("20"))
                self.assertEqual(cli("--category", "missing")["count"], 0)
            elif task == "feature":
                for threshold, count, total in (
                    ("10", 2, "32.50"),
                    ("12.50", 2, "32.50"),
                    ("0", 3, "40"),
                    ("100", 0, "0"),
                ):
                    result = cli("--min-amount", threshold)
                    self.assertEqual(result["count"], count)
                    self.assertEqual(Decimal(result["total"]), Decimal(total))
                result = cli("--category", "food", "--min-amount", "10")
                self.assertEqual(result["count"], 1)
                self.assertEqual(Decimal(result["total"]), Decimal("12.50"))
            elif task == "refactor":
                from expense_report.filters import normalize_category as filter_normalize
                from expense_report.report import normalize_category as report_normalize

                self.assertIs(filter_normalize, report_normalize)
                self.assertEqual(filter_normalize(" FOOD "), "food")
                definitions = [
                    node
                    for path in (workspace / "expense_report").glob("*.py")
                    for node in ast.walk(ast.parse(path.read_text()))
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                    and node.name == "normalize_category"
                ]
                self.assertEqual(len(definitions), 1)
                self.assertEqual(len(select_category(rows, " FOOD ")), 0)
                self.assertEqual(
                    build_report(rows, "GBP")["categories"], {"food": "20.00", "travel": "20.00"}
                )
            elif task == "documentation-config":
                self.assertEqual(
                    json.loads((workspace / "config.json").read_text())["currency"], "EUR"
                )
                readme = (workspace / "README.md").read_text()
                self.assertIn("EUR", readme)
                self.assertNotIn("USD", readme)
                self.assertEqual(cli()["currency"], "EUR")
            else:
                self.fail(f"unknown task: {task}")

        def test_preserved_behavior(self):
            result = cli("--currency", "GBP")
            self.assertEqual(result["currency"], "GBP")
            self.assertEqual(result["count"], 3)
            self.assertEqual(Decimal(result["total"]), Decimal("40"))

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Acceptance)
    return unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful()


if __name__ == "__main__":
    try:
        passed = evaluate(sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3]).read_text())
    except Exception as error:
        print(f"Evaluation failed: {type(error).__name__}: {error}", file=sys.stderr)
        passed = False
    raise SystemExit(0 if passed else 1)

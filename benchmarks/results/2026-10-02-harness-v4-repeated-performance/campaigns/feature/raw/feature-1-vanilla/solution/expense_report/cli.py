import argparse
from decimal import Decimal
import json
from pathlib import Path

from expense_report.filters import select_category, select_min_amount
from expense_report.report import build_report
from expense_report.storage import load_expenses


def main():
    parser = argparse.ArgumentParser(description="Summarize a CSV expense file.")
    parser.add_argument("path")
    parser.add_argument("--category")
    parser.add_argument("--currency")
    parser.add_argument("--min-amount", type=Decimal)
    args = parser.parse_args()
    config = json.loads((Path(__file__).resolve().parents[1] / "config.json").read_text())
    expenses = select_category(load_expenses(args.path), args.category)
    expenses = select_min_amount(expenses, args.min_amount)
    print(json.dumps(build_report(expenses, args.currency or config["currency"])))


if __name__ == "__main__":
    main()

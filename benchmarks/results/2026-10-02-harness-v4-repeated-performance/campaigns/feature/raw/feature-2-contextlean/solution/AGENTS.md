# Expense report repository

Dependency-free Python CLI for CSV expenses. Keep amounts as `decimal.Decimal`.

## Project map

- `expense_report/cli.py`: argument parsing and orchestration.
- `expense_report/storage.py`: CSV loading and decimal conversion.
- `expense_report/filters.py`: category selection.
- `expense_report/report.py`: totals and category grouping.
- `config.json`: default currency; CLI overrides take precedence.
- `tests/test_expenses.py`: unit tests and CLI checks.
- `README.md`: usage; `data/sample.csv`: example input.

## Verification and changes

Run `python3 -m unittest discover -s tests -v` from the repository root.
The example CLI is `python3 -m expense_report.cli data/sample.csv`.
Search the responsible module and its tests first. Preserve public imports and
decimal precision. Use the standard library. Update this map only if ownership,
paths or commands change; add tests for changed behavior.

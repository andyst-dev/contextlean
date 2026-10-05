# Example bootstrapped expense-report project

Dependency-free Python CSV CLI using Decimal and unittest; preserve public imports.

## Project map

- `expense_report/cli.py`: arguments/configuration and orchestration.
- `expense_report/storage.py`: CSV loading and Decimal conversion.
- `expense_report/filters.py`: category normalization/selection.
- `expense_report/report.py`: normalized grouping and totals.
- `config.json`: default currency; CLI options override it.
- `tests/test_expenses.py`: loading, filtering, report and CLI regression tests.
- `data/sample.csv`: runnable input.
- `README.md`: usage/development; search relevant sections when needed.

Flow: CLI/config → loader → selection → report → JSON. Keep Decimal through totals.

## Commands and local context

- Targeted: `python3 -m unittest discover -s tests -p test_expenses.py -v`.
- Full: `python3 -m unittest discover -s tests -v` (currently the same module).
- CLI: `python3 -m expense_report.cli data/sample.csv`; add `--category food --currency GBP` to check options.
- No build/lint/format/type-check or package-manager configuration is present.
- `__pycache__/` is generated. Inspect when relevant; preserve samples/tests.

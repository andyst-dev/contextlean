# Expense report

A dependency-free Python tool that summarizes a CSV file with `category,amount`
columns. Amounts use decimal arithmetic. The configured default currency is USD;
`--currency` overrides it. Category totals are grouped without case sensitivity.
Use `--min-amount` to include only individual expenses at or above a decimal
threshold.

```sh
python3 -m expense_report.cli data/sample.csv
python3 -m expense_report.cli data/sample.csv --category food --currency GBP
python3 -m expense_report.cli data/sample.csv --min-amount 10
python3 -m unittest discover -s tests -v
```

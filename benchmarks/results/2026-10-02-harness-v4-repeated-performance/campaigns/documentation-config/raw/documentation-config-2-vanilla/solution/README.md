# Expense report

A dependency-free Python tool that summarizes a CSV file with `category,amount`
columns. Amounts use decimal arithmetic. The configured default currency is EUR;
`--currency` overrides it. Category totals are grouped without case sensitivity.

```sh
python3 -m expense_report.cli data/sample.csv
python3 -m expense_report.cli data/sample.csv --category food --currency GBP
python3 -m unittest discover -s tests -v
```

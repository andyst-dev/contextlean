import csv
from decimal import Decimal


def load_expenses(path):
    with open(path, newline="", encoding="utf-8") as handle:
        return [
            {"category": row["category"], "amount": Decimal(row["amount"])}
            for row in csv.DictReader(handle)
        ]

from decimal import Decimal

from expense_report.filters import normalize_category


def build_report(expenses, currency):
    categories = {}
    for expense in expenses:
        key = normalize_category(expense["category"])
        categories[key] = categories.get(key, Decimal("0")) + expense["amount"]
    return {
        "currency": currency,
        "count": len(expenses),
        "total": str(sum((item["amount"] for item in expenses), Decimal("0"))),
        "categories": {key: str(value) for key, value in sorted(categories.items())},
    }

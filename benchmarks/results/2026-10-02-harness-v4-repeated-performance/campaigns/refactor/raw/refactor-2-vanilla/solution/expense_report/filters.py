from expense_report.categories import normalize_category


def select_category(expenses, category):
    if category is None:
        return list(expenses)
    return [
        expense for expense in expenses
        if normalize_category(expense["category"]) == category
    ]

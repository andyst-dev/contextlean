def normalize_category(value):
    return value.strip().casefold()


def select_category(expenses, category):
    if category is None:
        return list(expenses)
    normalized_category = normalize_category(category)
    return [
        expense for expense in expenses
        if normalize_category(expense["category"]) == normalized_category
    ]

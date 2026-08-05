import re


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """Фильтрация данных по слову в описании."""
    pattern = re.compile(rf"\b{search}\b")
    return [
        item
        for item in data
        if "description" in item and pattern.search(item["description"])
    ]


def process_bank_operations(data: list[dict], categories: list) -> dict:
    """Подсчет количества операции по категориям из описания.
    Возвращает словарь вида {категория: количество}."""
    result = {category: 0 for category in categories}

    for operation in data:
        description = operation.get("description", "")

        for category in categories:
            if category.lower() in description.lower():
                result[category] += 1

    return result

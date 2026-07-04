from src.processing import filter_by_state, sort_by_date

# Исходные данные
user_data: list[dict] = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
]

# Фильтруем только выполненные операции
filtered = filter_by_state(user_data)

# Сортируем по дате (по умолчанию: новые сверху)
result = sort_by_date(filtered)

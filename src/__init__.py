from typing import Dict, List

import src.generators
from src.processing import filter_by_state, sort_by_date

# Исходные данные
user_data: List[Dict] = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"}
]

# Фильтруем только выполненные операции
filtered = filter_by_state(user_data)

# Сортируем по дате (по умолчанию: новые сверху)
result = sort_by_date(filtered)

# start - целое число, начальное значение диапазона по умолчанию = 1
# end - целое число, конечное значение диапазона по умолчанию = $10^{15}$
# Генерируем первые пять номеров карт
for card in src.generators.card_number_generator(1, 5):
    print(card)

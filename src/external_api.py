import os
import requests

API_URL = "https://api.apilayer.com/exchangerates_data/latest"
API_KEY = os.getenv("API_KEY")


def convert_to_rub(amount: float, currency_code: str = "RUB") -> float | None:
    """Возвращает сумму операции по умолчанию в рублях, по желанию можно поменять на другую валюту(float).

    Args:
        amount (float): Сумма операции.
        currency_code (str, optional): Код валюты. По умолчанию "RUB".

    Raises:
        ValueError: если валюта отличается от RUB и не удалось получить курс.

    Returns:
        float | None: Конвертированная сумма или исходная сумма для RUB.
               Возвращается None только в случае исключения при парсинге ответа."""

    if currency_code == "RUB":
        return amount

    params = {
        "access_key": API_KEY,
        "symbols": "RUB",
        "base": currency_code,
    }

    response = requests.get(API_URL, params=params)

    try:
        data = response.json()

        if not data["success"]:
            raise ValueError(
                f"[ERROR] Не удалось получить курс валюты {currency_code}: поле 'success' отсутствует."
            )

        exchange_rate = data["rates"].get("RUB")
        if exchange_rate is None:
            raise ValueError(
                f"[ERROR] Не удалось получить курс валюты {currency_code}: поле 'rates' отсутствует."
            )

        return round(amount * exchange_rate, 2)
    except Exception as e:
        print(f"Не удалось получить данные о курсе({e}). Используем исходную валюту.")
        return amount

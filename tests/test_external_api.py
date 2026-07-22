from unittest.mock import MagicMock, patch

import pytest

from src.external_api import convert_to_rub


def test_convert_usd_to_rub(mock_response):
    """Проверка успешного преобразования USD.
    Мы имитируем ситуацию, когда API вернул курс 90.5."""
    with patch("requests.get") as mock_get:
        mock_get.return_value = mock_response

        result = convert_to_rub(100.0, "USD")

    assert isinstance(result, float), "Функция должна вернуть число."
    assert result == 9050.0, f"Результат неверен! Получено: {result}, ожидалось: 9050.0"


@pytest.fixture(name="mock_response")
def fixture_mock_response():
    """Возвращает объект-мок ответа от сервера."""
    mock = MagicMock()
    mock.status_code = 200
    mock.json.return_value = {
        "success": True,
        "timestamp": 169000000,
        "base": "USD",
        "date": "2026-07-18",
        "rates": {"RUB": 90.5},
    }
    return mock


def test_currency_is_rub():
    """Проверяет, что для валюты RUB возвращается исходная сумма без изменений."""
    result = convert_to_rub(123.45, "RUB")
    assert isinstance(result, float), "Функция должна вернуть число."
    assert result == 123.45, f"Результат неверен! Получено: {result}, ожидалось: 123.45"


def test_server_returns_4xx_or_5xx():
    """Проверяет реакцию на ошибку HTTP уровня протокола.
    Например, если сервер временно недоступен или запрос некорректен."""
    mock = MagicMock()
    mock.status_code = 400
    mock.json.return_value = None

    with patch("requests.get", return_value=mock):
        result = convert_to_rub(100.0, currency_code="EUR")

    assert isinstance(result, float)
    assert result == 100.0, f"Результат неверен! Получено: {result}, ожидалось: 100.0"


def test_server_returns_success_false():
    """Проверяет реакцию на ответ сервера {"success": false}.
    Например, ошибка авторизации (неверный токен)."""
    mock = MagicMock()
    mock.status_code = 200
    mock.json.return_value = {
        "success": False,
        "error": {
            "code": 101,
            "type": "missing_access_key",
            "info": "You have not supplied an API Access Key!",
        },
    }

    with patch("requests.get", return_value=mock):
        result = convert_to_rub(100.0, currency_code="USD")

    assert isinstance(result, float)
    assert result == 100.0


def test_unknown_currency_with_empty_rates(mock_response):
    mock_response.json.return_value.update({"base": "CAD", "rates": {}})

    result = convert_to_rub(amount=100.0, currency_code="CAD")

    assert isinstance(result, float), "Функция должна вернуть число."
    assert result == 100.0, f"Результат неверен! Получено: {result}, ожидалось: 100.0"

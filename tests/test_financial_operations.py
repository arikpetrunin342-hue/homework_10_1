import os
from pathlib import Path
from unittest.mock import mock_open, patch

import pandas as pd
import pytest

from src.financial_operations import (read_csv_transactions,
                                      read_excel_transactions)


@pytest.fixture(scope="module")
def project_root():
    """Возвращает путь до корневой директории проекта."""
    current_dir = Path(__file__).parent.parent
    return current_dir


def test_read_csv_transactions(project_root):
    """Проверяет корректность работы функции чтения CSV-файла.

    Мы используем патчинг встроенной функции open(), чтобы не читать реальный файл,
    а подставить заранее заготовленные данные."""
    csv_data = (
        "id;state;date;amount;currency_name;currency_code\n"
        "650703;EXECUTED;2023-10-09T11:32:08;29740;Peso;COP\n"
        "359891;EXECUTED;2020-12-07T13:32:32;16210;Sol;PEN\n"
    )

    with patch("builtins.open", new_callable=mock_open, read_data=csv_data) as _:
        result = read_csv_transactions(str(project_root / "data" / "test.csv"))

    assert isinstance(result, list), "Функция должна возвращать список."
    assert (
        len(result) == 2
    ), "Количество транзакций должно быть равно количеству строк минус заголовок."

    first_transaction = result[0]
    expected_keys = ["id", "state", "date", "amount", "currency_name", "currency_code"]
    for key in expected_keys:
        assert (
            key in first_transaction
        ), f"Отсутствует ключ '{key}' в словаре транзакции."

    assert first_transaction["id"] == 650703
    assert first_transaction["amount"] == 29740
    assert first_transaction["currency_code"] == "COP"


def test_read_excel_transactions(project_root):
    """Проверяет корректность работы функции чтения Excel-файла.

    Здесь мы не можем использовать простой патчинг файла, так как pandas.read_excel()
    ожидает настоящий xlsx-документ. Поэтому создаем временный файл."""
    excel_file_path = str(project_root / "data" / "temp.xlsx")

    df = pd.DataFrame(
        {
            "id": [650703, 359891],
            "state": ["EXECUTED", "EXECUTED"],
            "date": ["2023-10-09T11:32:08", "2020-12-07T13:32:32"],
            "amount": [29740, 16210],
            "currency_name": ["Peso", "Sol"],
            "currency_code": ["COP", "PEN"],
        }
    )
    df.to_excel(excel_file_path, index=False)

    try:
        result = read_excel_transactions(excel_file_path)

        assert isinstance(result, list), "Функция должна возвращать список."
        assert (
            len(result) == 2
        ), "Количество транзакций должно быть равно количеству строк."

        first_transaction = result[0]
        expected_keys = [
            "id",
            "state",
            "date",
            "amount",
            "currency_name",
            "currency_code",
        ]
        for key in expected_keys:
            assert (
                key in first_transaction
            ), f"Отсутствует ключ '{key}' в словаре транзакции."

        assert type(first_transaction["id"]) is int or float, "ID должен быть числом."
        assert (
            type(first_transaction["amount"]) is int or float
        ), "Amount должен быть числом."

    finally:
        os.remove(excel_file_path)

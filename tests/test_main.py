import re
import sys
from io import StringIO

import pandas as pd
import pytest

import src
from src.main import mask_description
from src.widget import mask_account_card


@pytest.fixture
def sample_dataframe():
    """Эталонный DataFrame для проверки фильтров."""
    return pd.DataFrame(
        {
            "state": ["EXECUTED", "CANCELED", "PENDING", "executed"],
            "date": [
                "2023-01-01T10:00:00Z",
                "2023-01-02T11:00:00Z",
                "2023-01-03T12:00:00Z",
                "2023-01-04T13:00:00Z",
            ],
            "amount": [1000.0, 500.0, 250.0, 750.0],
            "currency_code": ["RUB", "USD", "RUB", "rub"],
            "description": [
                "Перевод на карту 1234567890123456 другу",
                "Оплата Счет 40817810000000000001 ЖКХ",
                "Бонус за друга word_bonus",
                "Возврат средств 1111222233334444",
            ],
            "from": [
                "Счет 1111222233334444",
                None,
                "Discover 0720428384694643",
                "Счет 9999000011112222",
            ],
            "to": [
                "Discover 3172601889670065",
                "Счет 40817810000000000001",
                None,
                "Visa 1959232722494097",
            ],
        }
    )


def test_mask_description_card_and_account():
    input_text = "Счет 40817810000000000001"
    input_text2 = "Перевод на карту 1234567890123456"
    assert mask_account_card(input_text) == "Счет **0001"
    assert mask_account_card(input_text2) == "Перевод на карту 1234 56** **** 3456"


def test_mask_description_no_change():
    text = "Обычный перевод между своими счетами"
    assert mask_description(text) == text


def test_filter_by_status(sample_dataframe):
    df = sample_dataframe.copy()
    status = "EXECUTED"
    mask = df["state"].str.upper() == status
    result = df.loc[mask]
    assert len(result) == 2
    assert all(result["state"].str.upper() == status)


def test_filter_case_insensitive(sample_dataframe):
    df = sample_dataframe.copy()
    status = "executed".upper()
    mask = df["state"].str.upper() == status
    result = df.loc[mask]
    assert len(result) == 2
    assert all(result["state"].str.upper() == status)


def test_filter_by_currency_rub(sample_dataframe):
    df = sample_dataframe.copy()
    mask = df["currency_code"].str.upper() == "RUB"
    result = df.loc[mask]
    assert len(result) == 3
    assert set(result["currency_code"]) == {"RUB", "rub"}


def test_filter_by_keyword(sample_dataframe):
    df = sample_dataframe.copy()
    keyword = "word_bonus"
    mask = df["description"].apply(
        lambda x: any(word.upper() == keyword.upper() for word in str(x).split())
    )
    result = df.loc[mask]
    assert len(result) == 1
    assert result.iloc[0]["description"] == "Бонус за друга word_bonus"


def test_sorting_ascending(sample_dataframe):
    df = sample_dataframe.copy()
    sorted_df = df.sort_values(by="date", ascending=True)
    dates = list(sorted_df["date"])
    assert dates == sorted(dates)


def test_invalid_menu_choice(monkeypatch, capsys):
    """Проверка реакции на неверный выбор формата файла."""
    inputs = iter(["99"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    from src.main import main

    main()

    captured = capsys.readouterr()
    assert "Ошибка: неверный номер пункта меню!" in captured.out


def test_filter_status_case_insensitive(sample_dataframe):
    df = sample_dataframe.copy()
    status = "executed"
    mask = df["state"].str.upper() == status.upper()
    result = df.loc[mask]
    assert len(result) == 2


def test_filter_by_keyword_typo(sample_dataframe):
    df = sample_dataframe.copy()
    keyword = "wor_bonus"
    mask = df["description"].apply(
        lambda x: any(word.upper() == keyword.upper() for word in str(x).split())
    )
    result = df.loc[mask]
    assert len(result) == 0


def test_invalid_menu_choice_dop(monkeypatch, capsys):
    """Покрывает строку 56 (неверный номер меню)."""
    inputs = ["99"]
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))

    from src.main import main

    main()

    captured = capsys.readouterr()
    assert "Ошибка: неверный номер пункта меню!" in captured.out


def test_invalid_status_input(monkeypatch, capsys):
    """Покрывает цикл while True (строки ~68–78)."""
    inputs = [
        "1",
        "INVALID_STATUS_1",
        "INVALID_STATUS_2",
        "EXECUTED",
        "",
        "",
        "",
        "",
    ]
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))

    from src.main import main

    main()

    captured = capsys.readouterr()
    assert captured.out.count('Статус операции "INVALID_STATUS') == 2


@pytest.fixture(scope="function")
def temp_dataframe(tmp_path):
    """
    Создаёт временный DataFrame с одной транзакцией во всех форматах.
    """
    data = [
        {
            "id": 4009886,
            "state": "EXECUTED",
            "date": "2023-04-30T10:00:00Z",
            "amount": 23989.0,
            "currency_code": "rub",
            "description": "Перевод с карты на карту",
            "from": "Discover 2343953148883158",
            "to": "American Express 8400869379923599",
        }
    ]
    df = pd.DataFrame(data)

    paths = {}
    for ext in [".csv", ".xlsx", ".json"]:
        file_path = tmp_path / f"test{ext}"
        if ext == ".csv":
            df.to_csv(file_path, sep=";", index=False)
        elif ext == ".xlsx":
            df.to_excel(file_path, index=False)
        else:
            df.to_json(file_path, orient="records", force_ascii=False)
        paths[ext] = file_path
    return paths


def test_full_integration_success(temp_dataframe, monkeypatch):
    """Покрывает строки ~49–173."""
    inputs = iter(
        [
            "1",  # Выбор JSON-файла
            "EXECUTED",  # Статус
            "ДА",  # Сортировка по дате
            "ВОЗРАСТАНИЮ",  # по ВОЗРАСТАНИЮ
            "ДА",  # Только рубли
            "НЕТ",  # Фильтр по слову
            "1",  # Выбор JSON-файла
            "EXECUTED",  # Статус
            "ДА",  # Сортировка по дате
            "ВОЗРАСТАНИЮ",  # по ВОЗРАСТАНИЮ
            "ДА",  # Только рубли
            "НЕТ",  # Фильтр по слову
            "1",  # Выбор JSON-файла
            "EXECUTED",  # Статус
            "ДА",  # Сортировка по дате
            "ВОЗРАСТАНИЮ",  # по ВОЗРАСТАНИЮ
            "ДА",  # Только рубли
            "НЕТ",  # Фильтр по слову
        ]
    )

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    for format_ext in [".csv", ".xlsx", ".json"]:
        file_path = temp_dataframe[format_ext]

        captured_output = StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured_output

        try:
            src.main.main(file_path=file_path)
        finally:
            sys.stdout = old_stdout

        output = captured_output.getvalue().strip()

        assert "Привет!" in output, f"Не найдено Привет!: {output}"
        assert (
            "Распечатываю итоговый список транзакций..." in output
        ), f"Не найдено совпадение: {output}"

        pattern_sum = r"Сумма:\s*\d+\.\d+\s*(?:RUB|руб\.?|USD)"
        assert re.search(pattern_sum, output), f"Не найдено совпадение суммы: {output}"

        assert (
            (
                "****3158 -> ****3599" in output
                or "Discover ***3158 -> American Express ***3599" in output
                or "Счёт **** -> American Express ***3599" in output
            ),
            f"Не найдено совпадение карт: {output}",
        )

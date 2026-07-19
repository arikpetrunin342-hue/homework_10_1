import json
from unittest.mock import patch

from src.utils import load_operations

def test_load_valid_json_list():
    """Проверка успешного сценария.
    Функция должна возвращать список транзакций из валидного JSON."""
    mock_data = [
        {"id": 1, "amount": 100},
        {"id": 2, "amount": -50}
    ]

    with patch("builtins.open") as mocked_file:
        mocked_file.return_value.__enter__.return_value.read.return_value = json.dumps(mock_data)

        result = load_operations("any/path.json")

    assert isinstance(result, list), f"Получено {type(result)}, ожидался list"
    assert len(result) == 2, "Ожидалось 2 записи"
    assert result[0]["id"] == 1, "ID первой транзакции должен быть равен 1"
    assert result == mock_data, "Список транзакций не совпадает с исходными данными"

def test_load_invalid_json_format():
    """Проверка поведения при повреждённом содержимом файла.
    Даже если файл существует, но содержит некорректные символы,
    функция должна вернуть пустой список."""
    corrupted_json = "{invalid}"

    with patch("builtins.open") as mocked_file:
        mocked_file.return_value.__enter__.return_value.read.return_value = corrupted_json

        result = load_operations("corrupted/file.json")

    assert result == [], "При ошибке парсинга должен возвращаться пустой список"

def test_load_empty_file():
    """Проверка пустого файла.
    Пустой файл ("") также считается ошибкой парсинга JSON."""
    empty_string = ""

    with patch("builtins.open") as mocked_file:
        mocked_file.return_value.__enter__.return_value.read.return_value = empty_string

        result = load_operations("empty/file.json")

    assert result == [], "Пустой файл должен приводить к возврату []"

def test_load_not_a_list():
    """Проверка формата данных.
    Даже если файл успешно открыт и распарсен,
    но там лежит не список (например, словарь),
    функция всё равно возвращает пустой список."""
    not_a_list = {"key": "value"}

    with patch("builtins.open") as mocked_file:
        mocked_file.return_value.__enter__.return_value.read.return_value = json.dumps(not_a_list)

        result = load_operations("notalist/file.json")

    assert result == [], "Если данные не являются списком, должен возвращаться []"

def test_load_nonexistent_file():
    """Проверка отсутствия файла.
    При попытке открыть несуществующий файл возникает FileNotFoundError."""
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = load_operations("nonexistent/file.json")

    assert result == [], "Отсутствие файла должно приводить к возврату []"

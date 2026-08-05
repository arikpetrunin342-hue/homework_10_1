from src.process_bank import process_bank_operations, process_bank_search

for_test = [
    {
        "id": 650703.0,
        "state": "EXECUTED",
        "date": 1693913432000,
        "amount": 16210.0,
        "currency_name": "Sol",
        "currency_code": "PEN",
        "from": "Счет 58803664561298323391",
        "to": "Счет 39745660563456619397",
        "description": "Перевод организации",
    },
    {
        "id": 3598919.0,
        "state": "EXECUTED",
        "date": 1607295658000,
        "amount": 29740.0,
        "currency_name": "Peso",
        "currency_code": "COP",
        "from": "Discover 3172601889670065",
        "to": "Discover 0720428384694643",
        "description": "Перевод с карты на карту",
    },
]


def test_process_bank_search():
    res = process_bank_search(for_test, "Перевод организации")
    assert res == [
        {
            "id": 650703.0,
            "state": "EXECUTED",
            "date": 1693913432000,
            "amount": 16210.0,
            "currency_name": "Sol",
            "currency_code": "PEN",
            "from": "Счет 58803664561298323391",
            "to": "Счет 39745660563456619397",
            "description": "Перевод организации",
        }
    ]


def test_process_bank_operations():
    res = process_bank_operations(for_test, ["Перевод с карты на карту"])
    assert res == {"Перевод с карты на карту": 1}

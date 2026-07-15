import pytest

example = [
    {"id": 41428829, "state": "EXECUTED"},
    {"id": 939719570, "state": "EXECUTED"},
    {"id": 594226727, "state": "CANCELED"},
    {"id": 615064591, "state": "CANCELED"},
]

no_execute = [{"id": 1, "state": "CANCELED"}, {"id": 2, "state": "COMPLETED"}]

example_data = [
    {"date": "2019-07-03T18:35:29.512364"},
    {"date": "2018-06-30T02:08:58.425572"},
    {"date": "2018-09-12T21:27:25.241689"},
    {"date": "2018-10-14T08:21:33.419441"},
    {"date": "2018-10-14T08:21:33.419441"},
]

banking_details = [
    {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {
            "amount": "9824.07",
            "currency": {"name": "USD", "code": "USD"},
        },
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702",
    },
    {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {
            "amount": "79114.93",
            "currency": {"name": "RUB", "code": "RUB"},
        },
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188",
    },
]


@pytest.fixture(
    params=[
        ("40817810500001234567", "**4567"),  # Стандартный номер
        ("408178105000012345677", "Вы ввели слишком много символов"),
        ("4081781050000123456", "Вы пропустили некоторое количество символов"),
        ("", ""),
        ("4081 7810 5000 0123 4567", "**4567"),
        ("S40817810500001234567!", "**4567"),
    ]
)
def account_data(request):
    return request.param


@pytest.fixture(
    params=[
        (
            example,
            "EXECUTED",
            [
                {"id": 41428829, "state": "EXECUTED"},
                {"id": 939719570, "state": "EXECUTED"},
            ],
        ),
        (
            example,
            "CANCELED",
            [
                {"id": 594226727, "state": "CANCELED"},
                {"id": 615064591, "state": "CANCELED"},
            ],
        ),
        ([], "EXECUTED", []),
        (example, "EXECUTE", []),
        ([], None, []),
        (no_execute, "EXECUTE", []),
    ]
)
def filter_fixture(request):
    return request.param


@pytest.fixture(
    params=[
        ("Счет 64686473678894779589", "Счет **9589"),
        ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
        ("Visa Gold 5999414228426353", "Visa Gold 5999 41** **** 6353"),
        ("", ""),
        (None, ""),
        ("Visa Gold 5999414228426353 ", "Visa Gold 5999 41** **** 6353"),
    ]
)
def mask_fixture(request):
    return request.param

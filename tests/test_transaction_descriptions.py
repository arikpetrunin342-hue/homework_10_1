import pytest
from src.generators import transaction_descriptions
from tests.conftest import banking_details


@pytest.mark.parametrize(["input_transactions", "expected"],
[
    ([], []),
    (banking_details, ['Перевод организации', 'Перевод со счета на счет']),
    ([{"id": 939719570,"state": "EXECUTED","date": "2018-06-30T02:08:58.425572","operationAmount": {"amount": "9824.07","currency": {"name": "USD","code": "USD"}},"description": "Перевод организации","from": "Счет 75106830613657916952","to": "Счет 11776614605963066702"}], ['Перевод организации']),
    ([banking_details[0]], ['Перевод организации'])
])
def test_transaction_descriptions(input_transactions, expected):
    i = list(transaction_descriptions(input_transactions))
    assert i == expected

@pytest.mark.parametrize(["transactions", "expected_len"],
[
    ([], 0),
    ([banking_details[0]], 1),
    (banking_details, 2)
])
def test_transaction_descriptions_input_sizes(transactions, expected_len):
    result = list(transaction_descriptions(transactions))
    assert len(result) == expected_len

import pytest
from src.masks import get_mask_account, get_mask_card_number


def test_get_mask_account(account_data):
    input_value, expected_result = account_data
    assert get_mask_account(input_value) == expected_result


def test_get_mask_card_number(card_fixture):
    value, expected = card_fixture
    assert get_mask_card_number(value) == expected

@pytest.mark.parametrize("old_number, update_number", (
        ("", ""),
        ("4123987654321098", "4123 98** **** 1098"),
        ("41239876543210980", "Номер слишком длинный")
))
def test_get_mask_card_number(old_number, update_number):
    assert get_mask_card_number(old_number) == update_number

import pytest

from src.masks import get_mask_account, get_mask_card_number


def test_get_mask_account(account_data):
    input_value, expected_result = account_data
    assert get_mask_account(input_value) == expected_result


@pytest.mark.parametrize(
    "old_number, update_number",
    [
        ("", ""),
        ("4123987654321098", "4123 98** **** 1098"),
        ("41239876543210980", "Номер слишком длинный"),
        ("4123 9876 5432 1098", "4123 98** **** 1098"),
        ("412398765432109", "Номер слишком короткий"),
        ("4123-9876-5432-1098", "4123 98** **** 1098"),
        ("4A123.9876F5432!1098", "4123 98** **** 1098"),
    ],
)
def test_get_mask_card_number(old_number, update_number):
    result = get_mask_card_number(old_number)
    assert result == update_number

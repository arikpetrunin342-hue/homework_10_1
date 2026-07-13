import pytest

from src.widget import get_date, mask_account_card


def test_mask_account_card(mask_fixture):
    value, result = mask_fixture
    assert mask_account_card(value) == result


def test_get_date(date_fixture):
    date, result_date = date_fixture
    assert get_date(date) == result_date


@pytest.mark.parametrize("input_date, result_date", [
        (None, ""),
        ("2023.02.29", ""),
        ("2024-02", "")
])
def test_get_date(input_date, result_date):
    assert get_date(input_date) == result_date

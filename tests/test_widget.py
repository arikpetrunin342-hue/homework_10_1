import pytest

from src.widget import get_date, mask_account_card


def test_mask_account_card(mask_fixture):
    value, result = mask_fixture
    assert mask_account_card(value) == result


@pytest.mark.parametrize(
    "input_date, result_date",
    [
        (None, ""),
        ("2023.02.29", ""),
        ("2024-02", ""),
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("", ""),
        ("2024-01-01", "01.01.2024"),
        ("2024-12-31", "31.12.2024"),
        ("2024-02-29", "29.02.2024"),
        ("2024-02-29!", "29.02.2024"),
    ],
)
def test_get_date(input_date, result_date):
    assert get_date(input_date) == result_date

import pytest

from src.generators import card_number_generator

max_card_number = int("9" * 16)


@pytest.mark.parametrize(
    ["start", "end", "expected_result"],
    [
        (1, 1, ["0000 0000 0000 0001"]),
        (1, 3, ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]),
    ],
)
def test_card_number_generator_success(start, end, expected_result):
    i = list(card_number_generator(start, end))
    assert i == expected_result


@pytest.mark.parametrize(
    ["start", "end", "exception_type", "error_message"],
    [
        (10, 1, ValueError, "Конечное значение должно быть больше начального."),
        ("a", 1, TypeError, "Аргументы должны быть целыми числами."),
        (
            -5,
            100,
            ValueError,
            "Номера карт должны быть в диапазоне от 1 до 9999999999999999",
        ),
        (
            1,
            99999999999999999,
            ValueError,
            "Номера карт должны быть в диапазоне от 1 до 9999999999999999",
        ),
    ],
)
def test_card_number_generator_validation(start, end, exception_type, error_message):
    with pytest.raises(exception_type, match=error_message):
        next(card_number_generator(start, end))

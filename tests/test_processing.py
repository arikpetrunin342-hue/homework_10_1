import pytest

from src.processing import filter_by_state, sort_by_date


def test_filter_by_state(filter_fixture):
    data, state, expected = filter_fixture
    assert filter_by_state(data, state) == expected


def test_sort_by_date(sort_fixture):
    data, sort, sort_data = sort_fixture
    assert sort_by_date(data, sort) == sort_data

@pytest.mark.parametrize("input_value, revers, result", [
        ([], True, []),
        ([], False, []),
        ([{"date": "2020-01-01"}], True, [{"date": "2020-01-01"}]),
        ([{"date": "2020-01-01"}], False, [{"date": "2020-01-01"}])
])
def test_sort_by_date(input_value, revers, result):
    assert sort_by_date(input_value, revers) == result

import pytest

from src.processing import filter_by_state, sort_by_date


def test_filter_by_state(filter_fixture):
    data, state, expected = filter_fixture
    assert filter_by_state(data, state) == expected


def test_sort_by_date(sort_fixture):
    data, sort, sort_data = sort_fixture
    assert sort_by_date(data, sort) == sort_data

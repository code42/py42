import pytest

from py42._internal.filters.alert_filter import (
    create_contains_filter_group,
    create_not_contains_filter_group,
)


@pytest.fixture
def alert_filter_creator(mocker):
    return mocker.patch("py42._internal.filters.alert_filter.create_query_filter")


def test_create_contains_filter_group_calls_create_query_filter_with_correct_values(
    alert_filter_creator
):
    term = "test_eq_term"
    value_list = ["item1", "item2"]
    create_contains_filter_group(term, value_list)
    op = "CONTAINS"
    alert_filter_creator.assert_called_once_with(term, op, value_list)


def test_create_not_contains_filter_group_calls_create_query_filter_with_correct_values(
    alert_filter_creator
):
    term = "test_eq_term"
    value_list = ["item1", "item2"]
    create_not_contains_filter_group(term, value_list)
    op = "DOES_NOT_CONTAIN"
    alert_filter_creator.assert_called_once_with(term, op, value_list)

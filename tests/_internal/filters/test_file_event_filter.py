import pytest

from py42._internal.filters.file_event_filter import (
    create_exists_filter_group,
    create_not_exists_filter_group,
)


@pytest.fixture
def file_event_filter_creator(mocker):
    return mocker.patch("py42._internal.filters.file_event_filter.create_query_filter")


def test_create_exists_filter_group_calls_create_query_filter_with_correct_values(
    file_event_filter_creator
):
    term = "test_eq_term"
    create_exists_filter_group(term)
    op = "EXISTS"
    file_event_filter_creator.assert_called_once_with(term, op)


def test_create_not_exists_filter_group_calls_create_query_filter_with_correct_values(
    file_event_filter_creator
):
    term = "test_is_in_term"
    create_not_exists_filter_group(term)
    op = "DOES_NOT_EXIST"
    file_event_filter_creator.assert_called_once_with(term, op)

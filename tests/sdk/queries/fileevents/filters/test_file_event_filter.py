from py42._internal.compat import str
from py42.sdk.queries.fileevents.file_event_query import (
    create_exists_filter_group,
    create_not_exists_filter_group,
)


def test_create_exists_filter_returns_filter_group_with_correct_json_representation():
    term = "test_eq_term"
    _group = create_exists_filter_group(term)
    assert (
        str(_group) == '{"filterClause":"AND", "filters":[{"operator":"EXISTS", '
        '"term":"test_eq_term", "value":null}]}'
    )


def test_create_not_exists_filter_returns_filter_group_with_correct_json_representation():
    term = "test_is_in_term"
    _group = create_not_exists_filter_group(term)
    assert (
        str(_group)
        == '{"filterClause":"AND", "filters":[{"operator":"DOES_NOT_EXIST", '
        '"term":"test_is_in_term", "value":null}]}'
    )

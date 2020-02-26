from py42._internal.compat import str
from py42._internal.filters.alert_filter import (
    create_contains_filter_group,
    create_not_contains_filter_group,
)


def test_create_contains_filter_group_returns_filter_group_with_correct_json_representation():
    term = "test_eq_term"
    value_list = ["item1", "item2"]
    _group = create_contains_filter_group(term, value_list)
    assert (
        str(_group) == '{"filterClause":"AND", "filters":[{"operator":"CONTAINS", '
        '"term":"test_eq_term", "value":"[\'item1\', \'item2\']"}]}'
    )


def test_create_not_contains_filter_group_returns_filter_group_with_correct_json_representation():
    term = "test_eq_term"
    value_list = ["item1", "item2"]
    _group = create_not_contains_filter_group(term, value_list)
    assert (
        str(_group) == '{"filterClause":"AND", "filters":[{"operator":"DOES_NOT_CONTAIN", '
        '"term":"test_eq_term", "value":"[\'item1\', \'item2\']"}]}'
    )

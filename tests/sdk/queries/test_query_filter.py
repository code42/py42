# -*- coding: utf-8 -*-

from py42._internal.compat import str
from py42.sdk.queries.query_filter import (
    QueryFilter,
    create_eq_filter_group,
    create_filter_group,
    create_in_range_filter_group,
    create_is_in_filter_group,
    create_not_eq_filter_group,
    create_not_in_filter_group,
    create_on_or_after_filter_group,
    create_on_or_before_filter_group,
    create_query_filter,
)

EVENT_FILTER_FIELD_NAME = "filter_field_name"
OPERATOR_STRING = "IS_IN"
VALUE_STRING = "value_example"
VALUE_UNICODE = u"您已经发现了秘密信息"

JSON_QUERY_FILTER = '{{"operator":"{0}", "term":"{1}", "value":"{2}"}}'.format(
    OPERATOR_STRING, EVENT_FILTER_FIELD_NAME, VALUE_STRING
)

JSON_FILTER_GROUP_BASE = '{{"filterClause":"{0}", "filters":[{1}]}}'
JSON_FILTER_GROUP_AND = JSON_FILTER_GROUP_BASE.format("AND", JSON_QUERY_FILTER)
JSON_FILTER_GROUP_OR = JSON_FILTER_GROUP_BASE.format("OR", JSON_QUERY_FILTER)


def test_query_filter_constructs_successfully():
    assert QueryFilter(EVENT_FILTER_FIELD_NAME, OPERATOR_STRING, VALUE_STRING)


def test_query_filter_str_outputs_correct_json_representation(query_filter):
    assert str(query_filter) == JSON_QUERY_FILTER


def test_query_filter_unicode_outputs_correct_json_representation(unicode_query_filter):
    expected = u'{{"operator":"{0}", "term":"{1}", "value":"{2}"}}'.format(
        OPERATOR_STRING, EVENT_FILTER_FIELD_NAME, VALUE_UNICODE
    )
    assert str(unicode_query_filter) == expected


def test_filter_group_constructs_successfully(query_filter):
    assert create_filter_group(query_filter, "AND")


def test_filter_group_str_gives_correct_json_representation(query_filter):
    assert str(create_filter_group([query_filter], "AND")) == JSON_FILTER_GROUP_AND


def test_filter_group_with_and_specified_str_gives_correct_json_representation(query_filter):
    assert str(create_filter_group([query_filter], "AND")) == JSON_FILTER_GROUP_AND


def test_filter_group_with_or_specified_str_gives_correct_json_representation(query_filter):
    assert str(create_filter_group([query_filter], "OR")) == JSON_FILTER_GROUP_OR


def test_filter_group_with_multiple_filters_str_gives_correct_json_representation(
    query_filter_list,
):
    filters_string = ",".join([JSON_QUERY_FILTER for _ in range(3)])
    json_multi_filter_group = JSON_FILTER_GROUP_BASE.format("AND", filters_string)
    assert str(create_filter_group(query_filter_list, "AND")) == json_multi_filter_group


def test_filter_group_with_multiple_filters_and_specified_str_gives_correct_json_representation(
    query_filter_list,
):
    filters_string = ",".join([JSON_QUERY_FILTER for _ in range(3)])
    json_multi_filter_group = JSON_FILTER_GROUP_BASE.format("AND", filters_string)
    assert str(create_filter_group(query_filter_list, "AND")) == json_multi_filter_group


def test_filter_group_with_multiple_filters_or_specified_str_gives_correct_json_representation(
    query_filter_list,
):
    filters_string = ",".join([JSON_QUERY_FILTER for _ in range(3)])
    json_multi_filter_group = JSON_FILTER_GROUP_BASE.format("OR", filters_string)
    assert str(create_filter_group(query_filter_list, "OR")) == json_multi_filter_group


def test_create_eq_filter_group_returns_obj_with_correct_json_representation():
    filter_group = create_eq_filter_group("eqterm", "eqvalue")
    assert (
        str(filter_group) == '{"filterClause":"AND",'
        ' "filters":[{"operator":"IS", "term":"eqterm", "value":"eqvalue"}]}'
    )


def test_create_is_in_filter_group_returns_obj_with_correct_json_representation():
    filter_group = create_is_in_filter_group("isinterm", ["isinvalue1", "isinvalue2"])
    assert (
        str(filter_group) == '{"filterClause":"OR",'
        ' "filters":[{"operator":"IS", "term":"isinterm", "value":"isinvalue1"},'
        '{"operator":"IS", "term":"isinterm", "value":"isinvalue2"}]}'
    )


def test_create_not_eq_filter_group_returns_obj_with_correct_json_representation():
    filter_group = create_not_eq_filter_group("noteqterm", "noteqvalue")
    assert (
        str(filter_group) == '{"filterClause":"AND",'
        ' "filters":[{"operator":"IS_NOT", "term":"noteqterm", "value":"noteqvalue"}]}'
    )


def test_create_not_in_filter_group_returns_obj_with_correct_json_representation():
    filter_group = create_not_in_filter_group("isinterm", ["isinvalue1", "isinvalue2"])
    assert (
        str(filter_group) == '{"filterClause":"AND",'
        ' "filters":[{"operator":"IS_NOT", "term":"isinterm", "value":"isinvalue1"},'
        '{"operator":"IS_NOT", "term":"isinterm", "value":"isinvalue2"}]}'
    )


def test_create_on_or_after_filter_group_returns_obj_with_correct_json_representation():
    filter_group = create_on_or_after_filter_group("onorafterterm", "onoraftervalue")
    assert (
        str(filter_group) == '{"filterClause":"AND",'
        ' "filters":[{"operator":"ON_OR_AFTER", "term":"onorafterterm", "value":"onoraftervalue"}]}'
    )


def test_create_on_or_before_filter_group_returns_obj_with_correct_json_representation():
    filter_group = create_on_or_before_filter_group("onorbeforeterm", "onorbeforevalue")
    assert (
        str(filter_group) == '{"filterClause":"AND",'
        ' "filters":[{"operator":"ON_OR_BEFORE", "term":"onorbeforeterm", "value":"onorbeforevalue"}]}'
    )


def test_create_in_range_filter_group_returns_obj_with_correct_json_representation():
    filter_group = create_in_range_filter_group("rangeterm", "beforevalue", "aftervalue")
    assert (
        str(filter_group) == '{"filterClause":"AND",'
        ' "filters":[{"operator":"ON_OR_AFTER", "term":"rangeterm", "value":"beforevalue"},'
        '{"operator":"ON_OR_BEFORE", "term":"rangeterm", "value":"aftervalue"}]}'
    )


def test_create_query_filter_returns_obj_with_correct_json_representation():
    query_filter = create_query_filter(EVENT_FILTER_FIELD_NAME, OPERATOR_STRING, VALUE_STRING)
    assert str(query_filter) == '{{"operator":"{0}", "term":"{1}", "value":"{2}"}}'.format(
        OPERATOR_STRING, EVENT_FILTER_FIELD_NAME, VALUE_STRING
    )

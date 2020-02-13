# -*- coding: utf-8 -*-

import py42
from py42._internal.compat import str
from py42._internal.query_filter import (
    QueryFilter,
    create_eq_filter_group,
    create_query_filter,
    create_filter_group,
    create_between_filter_group,
    create_is_in_filter_group,
    create_not_eq_filter_group,
    create_not_in_filter_group,
    create_on_or_after_filter_group,
    create_on_or_before_filter_group,
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


def test_create_eq_filter_group_calls_create_query_filter_with_correct_values(mocker):
    mocker.patch("py42._internal.query_filter.create_query_filter")
    term = "test_eq_term"
    create_eq_filter_group(term, "eqval")
    op = "IS"

    py42._internal.query_filter.create_query_filter.assert_called_once_with(
        term, op, "eqval"
    )


def test_create_is_in_filter_group_calls_create_query_filter_with_correct_values(mocker):
    mocker.patch("py42._internal.query_filter.create_query_filter")
    term = "test_is_in_term"
    create_is_in_filter_group(term, ["isinval1", "isinval2", "isinval3"])
    op = "IS"
    calls = [
        mocker.call(term, op, "isinval1"),
        mocker.call(term, op, "isinval2"),
        mocker.call(term, op, "isinval3"),
    ]

    py42._internal.query_filter.create_query_filter.assert_has_calls(
        calls, any_order=True
    )


def test_create_not_eq_filter_group_calls_create_query_filter_with_correct_values(mocker):
    mocker.patch("py42._internal.query_filter.create_query_filter")
    term = "test_not_eq_term"
    create_not_eq_filter_group(term, "noteqtval")
    op = "IS_NOT"

    py42._internal.query_filter.create_query_filter.assert_called_once_with(
        term, op, "noteqtval"
    )


def test_create_not_in_filter_group_calls_create_query_filter_with_correct_values(mocker):
    mocker.patch("py42._internal.query_filter.create_query_filter")
    term = "test_not_in_term"
    create_not_in_filter_group(term, ["notinval1", "notinval2", "notinval3"])
    op = "IS_NOT"
    calls = [
        mocker.call(term, op, "notinval1"),
        mocker.call(term, op, "notinval2"),
        mocker.call(term, op, "notinval3"),
    ]

    py42._internal.query_filter.create_query_filter.assert_has_calls(
        calls, any_order=True
    )


def test_create_on_or_before_filter_group_calls_create_query_filter_with_correct_values(
    mocker,
):
    mocker.patch("py42._internal.query_filter.create_query_filter")
    term = "test_on_or_before_term"
    create_on_or_before_filter_group(term, "test_formatted_time")
    op = "ON_OR_BEFORE"
    py42._internal.query_filter.create_query_filter.assert_called_once_with(
        term, op, "test_formatted_time"
    )


def test_create_on_or_after_filter_group_calls_create_query_filter_with_correct_values(mocker):
    mocker.patch("py42._internal.query_filter.create_query_filter")
    term = "test_on_or_after_term"
    create_on_or_after_filter_group(term, "test_formatted_time")
    op = "ON_OR_AFTER"
    py42._internal.query_filter.create_query_filter.assert_called_once_with(
        term, op, "test_formatted_time"
    )


def test_create_between_filter_group_calls_create_query_filter_with_correct_values(mocker):
    mocker.patch("py42._internal.query_filter.create_query_filter")
    term = "test_between_term"
    start_time = "start_time"
    end_time = "end_time"
    create_between_filter_group(term, start_time, end_time)
    calls = [
        mocker.call(term, "ON_OR_BEFORE", end_time),
        mocker.call(term, "ON_OR_AFTER", start_time),
    ]

    py42._internal.query_filter.create_query_filter.assert_has_calls(
        calls, any_order=True
    )


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
    filter_group = create_is_in_filter_group("isinterm", ["isinvalue1", "isinvalue2"])
    assert (
        str(filter_group) == '{"filterClause":"OR",'
        ' "filters":[{"operator":"IS", "term":"isinterm", "value":"isinvalue1"},'
        '{"operator":"IS", "term":"isinterm", "value":"isinvalue2"}]}'
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


def test_create_between_filter_group_returns_obj_with_correct_json_representation():
    filter_group = create_between_filter_group("rangeterm", "beforevalue", "aftervalue")
    assert (
        str(filter_group) == '{"filterClause":"AND",'
        ' "filters":[{"operator":"ON_OR_AFTER", "term":"rangeterm", "value":"beforevalue"},'
        '{"operator":"ON_OR_BEFORE", "term":"rangeterm", "value":"aftervalue"}]}'
    )


def test_create_query_filter_returns_obj_with_correct_json_representation():
    query_filter = create_query_filter(
        EVENT_FILTER_FIELD_NAME, OPERATOR_STRING, VALUE_STRING
    )
    assert str(query_filter) == '{{"operator":"{0}", "term":"{1}", "value":"{2}"}}'.format(
        OPERATOR_STRING, EVENT_FILTER_FIELD_NAME, VALUE_STRING
    )

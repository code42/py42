# -*- coding: utf-8 -*-

from datetime import datetime
from time import time

from .conftest import format_timestamp, format_datetime
from py42._internal.compat import str
from py42.sdk.alert_query import AlertQuery
from py42.sdk.alert_query import DateObserved, Actor, Severity, RuleName, Description, AlertState

_TENANT_ID = u"tenant-id"
JSON_QUERY_BASE = u'{{"tenantId":"{0}", "groupClause":"{1}", "groups":[{2}], "pgNum":{3}, "pgSize":{4}, "srtDir":"{5}", "srtKey":"{6}"}}'


def build_query_json(group_clause, group_list):
    return JSON_QUERY_BASE.format(_TENANT_ID, group_clause, group_list, 0, 100, "asc", "CreatedAt")


def test_alert_query_repr_does_not_throw_type_error():
    # On python 2, `repr` doesn't throw.
    # On python 3, if `repr` doesn't return type `str`, then an exception is thrown.
    try:
        _ = repr(AlertQuery(_TENANT_ID))
    except TypeError:
        assert False


def test_alert_query_constructs_successfully(event_filter_group):
    assert AlertQuery(event_filter_group)


def test_alert_query_str_with_single_filter_gives_correct_json_representation(event_filter_group,):
    alert_query = AlertQuery(_TENANT_ID, event_filter_group)
    json_query_str = build_query_json("AND", event_filter_group)
    assert str(alert_query) == json_query_str


def test_alert_query_unicode_with_single_filter_gives_correct_json_representation(
    unicode_event_filter_group,
):
    alert_query = AlertQuery(_TENANT_ID, unicode_event_filter_group)
    json_query_str = build_query_json("AND", unicode_event_filter_group)
    assert str(alert_query) == json_query_str


def test_alert_query_str_with_single_filter_and_specified_gives_correct_json_representation(
    event_filter_group,
):
    alert_query = AlertQuery(_TENANT_ID, event_filter_group, group_clause="AND")
    json_query_str = build_query_json("AND", event_filter_group)
    assert str(alert_query) == json_query_str


def test_alert_query_str_with_single_filter_or_specified_gives_correct_json_representation(
    event_filter_group,
):
    alert_query = AlertQuery(_TENANT_ID, event_filter_group, group_clause="OR")
    json_query_str = build_query_json("OR", event_filter_group)
    assert str(alert_query) == json_query_str


def test_alert_query_str_with_many_filters_gives_correct_json_representation(
    event_filter_group_list,
):
    alert_query = AlertQuery(_TENANT_ID, event_filter_group_list)
    json_query_str = build_query_json("AND", event_filter_group_list)
    assert str(alert_query) == json_query_str


def test_alert_query_str_with_many_filters_and_specified_gives_correct_json_representation(
    event_filter_group_list,
):
    alert_query = AlertQuery(_TENANT_ID, event_filter_group_list, group_clause="AND")
    json_query_str = build_query_json("AND", event_filter_group_list)
    assert str(alert_query) == json_query_str


def test_alert_query_str_with_many_filters_or_specified_gives_correct_json_representation(
    event_filter_group_list,
):
    alert_query = AlertQuery(_TENANT_ID, event_filter_group_list, group_clause="OR")
    json_query_str = build_query_json("OR", event_filter_group_list)
    assert str(alert_query) == json_query_str


def test_alert_query_str_with_page_num_gives_correct_json_representation(event_filter_group):
    alert_query = AlertQuery(_TENANT_ID, event_filter_group)
    alert_query.page_number = 5
    json_query_str = JSON_QUERY_BASE.format(
        _TENANT_ID, "AND", event_filter_group, 5, 100, "asc", "CreatedAt"
    )
    assert str(alert_query) == json_query_str


def test_alert_query_str_with_page_size_gives_correct_json_representation(event_filter_group):
    alert_query = AlertQuery(_TENANT_ID, event_filter_group)
    alert_query.page_size = 500
    json_query_str = JSON_QUERY_BASE.format(
        _TENANT_ID, "AND", event_filter_group, 0, 500, "asc", "CreatedAt"
    )
    assert str(alert_query) == json_query_str


def test_alert_query_str_with_sort_direction_gives_correct_json_representation(event_filter_group,):
    alert_query = AlertQuery(_TENANT_ID, event_filter_group)
    alert_query.sort_direction = "desc"
    json_query_str = JSON_QUERY_BASE.format(
        _TENANT_ID, "AND", event_filter_group, 0, 100, "desc", "CreatedAt"
    )
    assert str(alert_query) == json_query_str


def test_alert_query_str_with_sort_key_gives_correct_json_representation(event_filter_group):
    alert_query = AlertQuery(_TENANT_ID, event_filter_group)
    alert_query.sort_key = "some_field_to_sort_by"
    json_query_str = JSON_QUERY_BASE.format(
        _TENANT_ID, "AND", event_filter_group, 0, 100, "asc", "some_field_to_sort_by"
    )
    assert str(alert_query) == json_query_str


def test_date_observed_on_or_after_str_gives_correct_json_representation():
    test_time = time()
    formatted = format_timestamp(test_time)
    _filter = DateObserved.on_or_after(test_time)
    expected = (
        '{{"filterClause":"AND", '
        '"filters":[{{"operator":"ON_OR_AFTER", "term":"CreatedAt", "value":"{0}"}}]'
        "}}".format(formatted)
    )
    assert str(_filter) == expected


def test_date_observed_on_or_before_str_gives_correct_json_representation():
    test_time = time()
    formatted = format_timestamp(test_time)
    _filter = DateObserved.on_or_before(test_time)
    expected = (
        '{{"filterClause":"AND", '
        '"filters":[{{"operator":"ON_OR_BEFORE", "term":"CreatedAt", "value":"{0}"}}]'
        "}}".format(formatted)
    )
    assert str(_filter) == expected


def test_date_observed_in_range_str_gives_correct_json_representation():
    test_before_time = time()
    test_after_time = time() + 30  # make sure timestamps are actually different
    formatted_before = format_timestamp(test_before_time)
    formatted_after = format_timestamp(test_after_time)
    _filter = DateObserved.in_range(test_before_time, test_after_time)
    expected = (
        '{{"filterClause":"AND", '
        '"filters":[{{"operator":"ON_OR_AFTER", "term":"CreatedAt", "value":"{0}"}},'
        '{{"operator":"ON_OR_BEFORE", "term":"CreatedAt", "value":"{1}"}}]}}'.format(
            formatted_before, formatted_after
        )
    )
    assert str(_filter) == expected


def test_date_observed_on_same_day_str_gives_correct_json_representation():
    test_time = time()
    test_date = datetime.utcfromtimestamp(test_time)
    start_time = datetime(test_date.year, test_date.month, test_date.day, 0, 0, 0)
    end_time = datetime(test_date.year, test_date.month, test_date.day, 23, 59, 59)
    formatted_before = format_datetime(start_time)
    formatted_after = format_datetime(end_time)

    _filter = DateObserved.on_same_day(test_time)
    expected = (
        '{{"filterClause":"AND", '
        '"filters":[{{"operator":"ON_OR_AFTER", "term":"CreatedAt", "value":"{0}"}},'
        '{{"operator":"ON_OR_BEFORE", "term":"CreatedAt", "value":"{1}"}}]}}'.format(
            formatted_before, formatted_after
        )
    )
    assert str(_filter) == expected


def test_actor_eq_str_gives_correct_json_representation():
    _filter = Actor.eq("test.testerson")
    expected = (
        '{"filterClause":"AND", '
        '"filters":[{"operator":"IS", "term":"actor", "value":"test.testerson"}]}'
    )
    assert str(_filter) == expected


def test_actor_not_eq_str_gives_correct_json_representation():
    _filter = Actor.not_eq("test.testerson")
    expected = (
        '{"filterClause":"AND", '
        '"filters":[{"operator":"IS_NOT", "term":"actor", "value":"test.testerson"}]}'
    )
    assert str(_filter) == expected


def test_actor_is_in_str_gives_correct_json_representation():
    items = ["test.testerson", "flag.flagerson", "mock.mockerson"]
    _filter = Actor.is_in(items)
    expected = (
        '{"filterClause":"OR", '
        '"filters":[{"operator":"IS", "term":"actor", "value":"test.testerson"},'
        '{"operator":"IS", "term":"actor", "value":"flag.flagerson"},'
        '{"operator":"IS", "term":"actor", "value":"mock.mockerson"}]}'
    )
    assert str(_filter) == expected


def test_actor_not_in_str_gives_correct_json_representation():
    items = ["test.testerson", "flag.flagerson", "mock.mockerson"]
    _filter = Actor.not_in(items)
    expected = (
        '{"filterClause":"AND", '
        '"filters":[{"operator":"IS_NOT", "term":"actor", "value":"test.testerson"},'
        '{"operator":"IS_NOT", "term":"actor", "value":"flag.flagerson"},'
        '{"operator":"IS_NOT", "term":"actor", "value":"mock.mockerson"}]}'
    )
    assert str(_filter) == expected


def test_actor_contains_str_gives_correct_json_representation():
    _filter = Actor.contains("test")
    expected = (
        '{"filterClause":"AND", '
        '"filters":[{"operator":"CONTAINS", "term":"actor", "value":"test"}]}'
    )
    assert str(_filter) == expected


def test_actor_not_contains_str_gives_correct_json_representation():
    _filter = Actor.not_contains("test")
    expected = (
        '{"filterClause":"AND", '
        '"filters":[{"operator":"DOES_NOT_CONTAIN", "term":"actor", "value":"test"}]}'
    )
    assert str(_filter) == expected


def test_severity_eq_str_gives_correct_json_representation():
    _filter = Severity.eq("HIGH")
    expected = (
        '{"filterClause":"AND", "filters":[{"operator":"IS", "term":"severity", "value":"HIGH"}]}'
    )
    assert str(_filter) == expected


def test_severity_not_eq_str_gives_correct_json_representation():
    _filter = Severity.not_eq("HIGH")
    expected = (
        '{"filterClause":"AND", '
        '"filters":[{"operator":"IS_NOT", "term":"severity", "value":"HIGH"}]}'
    )
    assert str(_filter) == expected


def test_severity_is_in_str_gives_correct_json_representation():
    _filter = Severity.is_in(["HIGH", "LOW"])
    expected = (
        '{"filterClause":"OR", '
        '"filters":[{"operator":"IS", "term":"severity", "value":"HIGH"},'
        '{"operator":"IS", "term":"severity", "value":"LOW"}]}'
    )
    assert str(_filter) == expected


def test_severity_not_in_str_gives_correct_json_representation():
    _filter = Severity.not_in(["HIGH", "LOW"])
    expected = (
        '{"filterClause":"AND", '
        '"filters":[{"operator":"IS_NOT", "term":"severity", "value":"HIGH"},'
        '{"operator":"IS_NOT", "term":"severity", "value":"LOW"}]}'
    )
    assert str(_filter) == expected


def test_rule_name_eq_str_gives_correct_json_representation():
    _filter = RuleName.eq("Departing Employee")
    expected = (
        '{"filterClause":"AND", '
        '"filters":[{"operator":"IS", "term":"name", "value":"Departing Employee"}]}'
    )
    assert str(_filter) == expected


def test_rule_name_not_eq_str_gives_correct_json_representation():
    _filter = RuleName.not_eq("Departing Employee")
    expected = (
        '{"filterClause":"AND", '
        '"filters":[{"operator":"IS_NOT", "term":"name", "value":"Departing Employee"}]}'
    )
    assert str(_filter) == expected


def test_rule_name_is_in_str_gives_correct_json_representation():
    items = ["rule 1", "rule 2", "rule 3"]
    _filter = RuleName.is_in(items)
    expected = (
        '{"filterClause":"OR", '
        '"filters":[{"operator":"IS", "term":"name", "value":"rule 1"},'
        '{"operator":"IS", "term":"name", "value":"rule 2"},'
        '{"operator":"IS", "term":"name", "value":"rule 3"}]}'
    )
    assert str(_filter) == expected


def test_rule_name_not_in_str_gives_correct_json_representation():
    items = ["rule 1", "rule 2", "rule 3"]
    _filter = RuleName.not_in(items)
    expected = (
        '{"filterClause":"AND", '
        '"filters":[{"operator":"IS_NOT", "term":"name", "value":"rule 1"},'
        '{"operator":"IS_NOT", "term":"name", "value":"rule 2"},'
        '{"operator":"IS_NOT", "term":"name", "value":"rule 3"}]}'
    )
    assert str(_filter) == expected


def test_rule_name_contains_str_gives_correct_json_representation():
    _filter = RuleName.contains("test")
    expected = (
        '{"filterClause":"AND", "filters":[{"operator":"CONTAINS", "term":"name", "value":"test"}]}'
    )
    assert str(_filter) == expected


def test_rule_name_not_contains_str_gives_correct_json_representation():
    _filter = RuleName.not_contains("test")
    expected = (
        '{"filterClause":"AND", '
        '"filters":[{"operator":"DOES_NOT_CONTAIN", "term":"name", "value":"test"}]}'
    )
    assert str(_filter) == expected


def test_description_eq_str_gives_correct_json_representation():
    _filter = Description.eq("Departing Employee")
    expected = (
        '{"filterClause":"AND", '
        '"filters":[{"operator":"IS", "term":"description", "value":"Departing Employee"}]}'
    )
    assert str(_filter) == expected


def test_description_not_eq_str_gives_correct_json_representation():
    _filter = Description.not_eq("Departing Employee")
    expected = (
        '{"filterClause":"AND", '
        '"filters":[{"operator":"IS_NOT", "term":"description", "value":"Departing Employee"}]}'
    )
    assert str(_filter) == expected


def test_description_is_in_str_gives_correct_json_representation():
    items = ["rule 1", "rule 2", "rule 3"]
    _filter = Description.is_in(items)
    expected = (
        '{"filterClause":"OR", '
        '"filters":[{"operator":"IS", "term":"description", "value":"rule 1"},'
        '{"operator":"IS", "term":"description", "value":"rule 2"},'
        '{"operator":"IS", "term":"description", "value":"rule 3"}]}'
    )
    assert str(_filter) == expected


def test_description_not_in_str_gives_correct_json_representation():
    items = ["rule 1", "rule 2", "rule 3"]
    _filter = Description.not_in(items)
    expected = (
        '{"filterClause":"AND", '
        '"filters":[{"operator":"IS_NOT", "term":"description", "value":"rule 1"},'
        '{"operator":"IS_NOT", "term":"description", "value":"rule 2"},'
        '{"operator":"IS_NOT", "term":"description", "value":"rule 3"}]}'
    )
    assert str(_filter) == expected


def test_description_contains_str_gives_correct_json_representation():
    _filter = Description.contains("test")
    expected = (
        '{"filterClause":"AND", '
        '"filters":[{"operator":"CONTAINS", "term":"description", "value":"test"}]}'
    )
    assert str(_filter) == expected


def test_description_not_contains_str_gives_correct_json_representation():
    _filter = Description.not_contains("test")
    expected = (
        '{"filterClause":"AND", '
        '"filters":[{"operator":"DOES_NOT_CONTAIN", "term":"description", "value":"test"}]}'
    )
    assert str(_filter) == expected


def test_alert_state_eq_str_gives_correct_json_representation():
    _filter = AlertState.eq("OPEN")
    expected = (
        '{"filterClause":"AND", "filters":[{"operator":"IS", "term":"state", "value":"OPEN"}]}'
    )
    assert str(_filter) == expected


def test_alert_state_not_eq_str_gives_correct_json_representation():
    _filter = AlertState.not_eq("OPEN")
    expected = (
        '{"filterClause":"AND", "filters":[{"operator":"IS_NOT", "term":"state", "value":"OPEN"}]}'
    )
    assert str(_filter) == expected


def test_alert_state_is_in_str_gives_correct_json_representation():
    items = ["OPEN", "DISMISSED"]
    _filter = AlertState.is_in(items)
    expected = (
        '{"filterClause":"OR", '
        '"filters":[{"operator":"IS", "term":"state", "value":"OPEN"},'
        '{"operator":"IS", "term":"state", "value":"DISMISSED"}]}'
    )
    assert str(_filter) == expected


def test_alert_state_not_in_str_gives_correct_json_representation():
    items = ["OPEN", "DISMISSED"]
    _filter = AlertState.not_in(items)
    expected = (
        '{"filterClause":"AND", '
        '"filters":[{"operator":"IS_NOT", "term":"state", "value":"OPEN"},'
        '{"operator":"IS_NOT", "term":"state", "value":"DISMISSED"}]}'
    )
    assert str(_filter) == expected

# -*- coding: utf-8 -*-

from py42._internal.compat import str
from py42.sdk.alert_query import AlertQuery

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


def test_alert_query_str_with_single_filter_gives_correct_json_representation(
    event_filter_group,
):
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
    json_query_str = JSON_QUERY_BASE.format(_TENANT_ID, "AND", event_filter_group, 5, 100, "asc", "CreatedAt")
    assert str(alert_query) == json_query_str


def test_alert_query_str_with_page_size_gives_correct_json_representation(event_filter_group):
    alert_query = AlertQuery(_TENANT_ID, event_filter_group)
    alert_query.page_size = 500
    json_query_str = JSON_QUERY_BASE.format(_TENANT_ID, "AND", event_filter_group, 0, 500, "asc", "CreatedAt")
    assert str(alert_query) == json_query_str


def test_alert_query_str_with_sort_direction_gives_correct_json_representation(
    event_filter_group,
):
    alert_query = AlertQuery(_TENANT_ID, event_filter_group)
    alert_query.sort_direction = "desc"
    json_query_str = JSON_QUERY_BASE.format(_TENANT_ID, "AND", event_filter_group, 0, 100, "desc", "CreatedAt")
    assert str(alert_query) == json_query_str


def test_alert_query_str_with_sort_key_gives_correct_json_representation(event_filter_group):
    alert_query = AlertQuery(_TENANT_ID, event_filter_group)
    alert_query.sort_key = "some_field_to_sort_by"
    json_query_str = JSON_QUERY_BASE.format(
        _TENANT_ID, "AND", event_filter_group, 0, 100, "asc", "some_field_to_sort_by"
    )
    assert str(alert_query) == json_query_str

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


def test_date_observed_on_or_after_sets_filter_properties_correctly(on_or_after_filter_creator,):
    test_time = time()
    formatted = format_timestamp(test_time)
    DateObserved.on_or_after(test_time)
    on_or_after_filter_creator.assert_called_once_with("CreatedAt", formatted)


def test_date_observed_on_or_before_sets_filter_properties_correctly(on_or_before_filter_creator,):
    test_time = time()
    formatted = format_timestamp(test_time)
    DateObserved.on_or_before(test_time)
    on_or_before_filter_creator.assert_called_once_with("CreatedAt", formatted)


def test_date_observed_in_range_sets_filter_properties_correctly(in_range_filter_creator):
    test_before_time = time()
    test_after_time = time() + 30  # make sure timestamps are actually different
    formatted_before = format_timestamp(test_before_time)
    formatted_after = format_timestamp(test_after_time)
    DateObserved.in_range(test_before_time, test_after_time)
    in_range_filter_creator.assert_called_once_with("CreatedAt", formatted_before, formatted_after)


def test_date_observed_on_sets_filter_properties_correctly(in_range_filter_creator):
    test_time = time()
    test_date = datetime.utcfromtimestamp(test_time)
    start_time = datetime(test_date.year, test_date.month, test_date.day, 0, 0, 0)
    end_time = datetime(test_date.year, test_date.month, test_date.day, 0, 23, 59)
    formatted_before = format_datetime(start_time)
    formatted_after = format_datetime(end_time)

    DateObserved.on(test_time)
    in_range_filter_creator.assert_called_once_with("CreatedAt", formatted_before, formatted_after)


def test_actor_exists_sets_filter_properties_correctly(exists_filter_creator):
    Actor.exists()
    exists_filter_creator.assert_called_once_with("actor")


def test_actor_not_exists_sets_filter_properties_correctly(not_exists_filter_creator):
    Actor.not_exists()
    not_exists_filter_creator.assert_called_once_with("actor")


def test_actor_eq_sets_filter_properties_correctly(eq_filter_creator):
    Actor.eq("test.testerson")
    eq_filter_creator.assert_called_once_with("fileName", "actor")


def test_actor_not_eq_sets_filter_properties_correctly(not_eq_filter_creator):
    Actor.not_eq("test.testerson")
    not_eq_filter_creator.assert_called_once_with("fileName", "actor")


def test_actor_is_in_sets_filter_properties_correctly(is_in_filter_creator):
    items = ["test.testerson", "flag.flagerson", "mock.mockerson"]
    Actor.is_in(items)
    is_in_filter_creator.assert_called_once_with("actor", items)


def test_actor_not_in_sets_filter_properties_correctly(not_in_filter_creator):
    items = ["test.testerson", "flag.flagerson", "mock.mockerson"]
    Actor.not_in(items)
    not_in_filter_creator.assert_called_once_with("actor", items)

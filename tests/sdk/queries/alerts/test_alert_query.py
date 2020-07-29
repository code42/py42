# -*- coding: utf-8 -*-
from datetime import datetime
from time import time

from tests.sdk.queries.conftest import CONTAINS
from tests.sdk.queries.conftest import format_datetime
from tests.sdk.queries.conftest import format_timestamp
from tests.sdk.queries.conftest import IN_RANGE
from tests.sdk.queries.conftest import IS
from tests.sdk.queries.conftest import IS_IN
from tests.sdk.queries.conftest import IS_NOT
from tests.sdk.queries.conftest import NOT_CONTAINS
from tests.sdk.queries.conftest import NOT_IN
from tests.sdk.queries.conftest import ON_OR_AFTER
from tests.sdk.queries.conftest import ON_OR_BEFORE

from py42._compat import str
from py42.sdk.queries.alerts.alert_query import AlertQuery
from py42.sdk.queries.alerts.filters import Actor
from py42.sdk.queries.alerts.filters import AlertState
from py42.sdk.queries.alerts.filters import DateObserved
from py42.sdk.queries.alerts.filters import Description
from py42.sdk.queries.alerts.filters import RuleId
from py42.sdk.queries.alerts.filters import RuleName
from py42.sdk.queries.alerts.filters import RuleSource
from py42.sdk.queries.alerts.filters import RuleType
from py42.sdk.queries.alerts.filters import Severity

_TENANT_ID = u"null"
JSON_QUERY_BASE = u'{{"tenantId": {0}, "groupClause":"{1}", "groups":[{2}], "pgNum":{3}, "pgSize":{4}, "srtDirection":"{5}", "srtKey":"{6}"}}'


def build_query_json(group_clause, group_list):
    return JSON_QUERY_BASE.format(
        _TENANT_ID, group_clause, group_list, 0, 500, "desc", "CreatedAt"
    )


def test_alert_query_repr_does_not_throw_type_error():
    # On python 2, `repr` doesn't throw.
    # On python 3, if `repr` doesn't return type `str`, then an exception is thrown.
    try:
        _ = repr(AlertQuery())
    except TypeError:
        raise AssertionError()


def test_alert_query_constructs_successfully(event_filter_group):
    assert AlertQuery(event_filter_group)


def test_alert_query_str_with_single_filter_gives_correct_json_representation(
    event_filter_group,
):
    alert_query = AlertQuery(event_filter_group)
    json_query_str = build_query_json("AND", event_filter_group)
    assert str(alert_query) == json_query_str


def test_alert_query_unicode_with_single_filter_gives_correct_json_representation(
    unicode_event_filter_group,
):
    alert_query = AlertQuery(unicode_event_filter_group)
    json_query_str = build_query_json("AND", unicode_event_filter_group)
    assert str(alert_query) == json_query_str


def test_alert_query_str_with_single_filter_and_specified_gives_correct_json_representation(
    event_filter_group,
):
    alert_query = AlertQuery(event_filter_group, group_clause="AND")
    json_query_str = build_query_json("AND", event_filter_group)
    assert str(alert_query) == json_query_str


def test_alert_query_str_with_single_filter_or_specified_gives_correct_json_representation(
    event_filter_group,
):
    alert_query = AlertQuery(event_filter_group, group_clause="OR")
    json_query_str = build_query_json("OR", event_filter_group)
    assert str(alert_query) == json_query_str


def test_alert_query_str_with_many_filters_gives_correct_json_representation(
    event_filter_group_list,
):
    alert_query = AlertQuery(event_filter_group_list)
    json_query_str = build_query_json("AND", event_filter_group_list)
    assert str(alert_query) == json_query_str


def test_alert_query_str_with_many_filters_and_specified_gives_correct_json_representation(
    event_filter_group_list,
):
    alert_query = AlertQuery(event_filter_group_list, group_clause="AND")
    json_query_str = build_query_json("AND", event_filter_group_list)
    assert str(alert_query) == json_query_str


def test_alert_query_str_with_many_filters_or_specified_gives_correct_json_representation(
    event_filter_group_list,
):
    alert_query = AlertQuery(event_filter_group_list, group_clause="OR")
    json_query_str = build_query_json("OR", event_filter_group_list)
    assert str(alert_query) == json_query_str


def test_alert_query_str_with_page_num_gives_correct_json_representation(
    event_filter_group,
):
    alert_query = AlertQuery(event_filter_group)
    alert_query.page_number = 5
    json_query_str = JSON_QUERY_BASE.format(
        _TENANT_ID, "AND", event_filter_group, 5, 500, "desc", "CreatedAt"
    )
    assert str(alert_query) == json_query_str


def test_alert_query_str_with_page_size_gives_correct_json_representation(
    event_filter_group,
):
    alert_query = AlertQuery(event_filter_group)
    alert_query.page_size = 250
    json_query_str = JSON_QUERY_BASE.format(
        _TENANT_ID, "AND", event_filter_group, 0, 250, "desc", "CreatedAt"
    )
    assert str(alert_query) == json_query_str


def test_alert_query_str_with_sort_direction_gives_correct_json_representation(
    event_filter_group,
):
    alert_query = AlertQuery(event_filter_group)
    alert_query.sort_direction = "asc"
    json_query_str = JSON_QUERY_BASE.format(
        _TENANT_ID, "AND", event_filter_group, 0, 500, "asc", "CreatedAt"
    )
    assert str(alert_query) == json_query_str


def test_alert_query_str_with_sort_key_gives_correct_json_representation(
    event_filter_group,
):
    alert_query = AlertQuery(event_filter_group)
    alert_query.sort_key = "some_field_to_sort_by"
    json_query_str = JSON_QUERY_BASE.format(
        _TENANT_ID, "AND", event_filter_group, 0, 500, "desc", "some_field_to_sort_by"
    )
    assert str(alert_query) == json_query_str


def test_alert_query_from_dict_gives_correct_json_representation():
    group = {
        "filterClause": "AND",
        "filters": [{"operator": "IS", "term": "testterm", "value": "testval"}],
    }
    group_str = '{"filterClause":"AND", "filters":[{"operator":"IS", "term":"testterm", "value":"testval"}]}'
    alert_query_dict = {"groupClause": "AND", "groups": [group]}
    alert_query = AlertQuery.from_dict(alert_query_dict)
    json_query_str = JSON_QUERY_BASE.format(
        _TENANT_ID, "AND", group_str, 0, 500, "desc", "CreatedAt"
    )
    assert str(alert_query) == json_query_str


def test_alert_query_dict_gives_expected_dict_representation(event_filter_group):
    alert_query = AlertQuery(event_filter_group)
    alert_query_query_dict = dict(alert_query)
    assert alert_query_query_dict["groupClause"] == "AND"
    assert alert_query_query_dict["pgNum"] == 0
    assert alert_query_query_dict["pgSize"] == 500
    assert alert_query_query_dict["srtDirection"] == "desc"
    assert alert_query_query_dict["srtKey"] == "CreatedAt"
    assert type(alert_query_query_dict["groups"]) == list


def test_date_observed_on_or_after_str_gives_correct_json_representation():
    test_time = time()
    formatted = format_timestamp(test_time)
    _filter = DateObserved.on_or_after(test_time)
    expected = ON_OR_AFTER.format("createdAt", formatted)
    assert str(_filter) == expected


def test_date_observed_on_or_before_str_gives_correct_json_representation():
    test_time = time()
    formatted = format_timestamp(test_time)
    _filter = DateObserved.on_or_before(test_time)
    expected = ON_OR_BEFORE.format("createdAt", formatted)
    assert str(_filter) == expected


def test_date_observed_in_range_str_gives_correct_json_representation():
    test_before_time = time()
    test_after_time = time() + 30  # make sure timestamps are actually different
    formatted_before = format_timestamp(test_before_time)
    formatted_after = format_timestamp(test_after_time)
    _filter = DateObserved.in_range(test_before_time, test_after_time)
    expected = IN_RANGE.format("createdAt", formatted_before, formatted_after)
    assert str(_filter) == expected


def test_date_observed_on_same_day_str_gives_correct_json_representation():
    test_time = time()
    test_date = datetime.utcfromtimestamp(test_time)
    start_time = datetime(test_date.year, test_date.month, test_date.day, 0, 0, 0)
    end_time = datetime(test_date.year, test_date.month, test_date.day, 23, 59, 59)
    formatted_before = format_datetime(start_time)
    formatted_after = format_datetime(end_time)
    _filter = DateObserved.on_same_day(test_time)
    expected = IN_RANGE.format("createdAt", formatted_before, formatted_after)
    assert str(_filter) == expected


def test_actor_eq_str_gives_correct_json_representation():
    _filter = Actor.eq("test.testerson")
    expected = IS.format("actor", "test.testerson")
    assert str(_filter) == expected


def test_actor_not_eq_str_gives_correct_json_representation():
    _filter = Actor.not_eq("test.testerson")
    expected = IS_NOT.format("actor", "test.testerson")
    assert str(_filter) == expected


def test_actor_is_in_str_gives_correct_json_representation():
    items = ["test.testerson", "flag.flagerson", "mock.mockerson"]
    _filter = Actor.is_in(items)
    expected = IS_IN.format("actor", *sorted(items))
    assert str(_filter) == expected


def test_actor_not_in_str_gives_correct_json_representation():
    items = ["test.testerson", "flag.flagerson", "mock.mockerson"]
    _filter = Actor.not_in(items)
    expected = NOT_IN.format("actor", *sorted(items))
    assert str(_filter) == expected


def test_actor_contains_str_gives_correct_json_representation():
    _filter = Actor.contains("test")
    expected = CONTAINS.format("actor", "test")
    assert str(_filter) == expected


def test_actor_not_contains_str_gives_correct_json_representation():
    _filter = Actor.not_contains("test")
    expected = NOT_CONTAINS.format("actor", "test")
    assert str(_filter) == expected


def test_severity_eq_str_gives_correct_json_representation():
    _filter = Severity.eq("HIGH")
    expected = IS.format("severity", "HIGH")
    assert str(_filter) == expected


def test_severity_not_eq_str_gives_correct_json_representation():
    _filter = Severity.not_eq("HIGH")
    expected = IS_NOT.format("severity", "HIGH")
    assert str(_filter) == expected


def test_severity_is_in_str_gives_correct_json_representation():
    items = ["HIGH", "MEDIUM", "LOW"]
    _filter = Severity.is_in(items)
    expected = IS_IN.format("severity", *sorted(items))
    assert str(_filter) == expected


def test_severity_not_in_str_gives_correct_json_representation():
    items = ["HIGH", "MEDIUM", "LOW"]
    _filter = Severity.not_in(items)
    expected = NOT_IN.format("severity", *sorted(items))
    assert str(_filter) == expected


def test_rule_name_eq_str_gives_correct_json_representation():
    _filter = RuleName.eq("Departing Employee")
    expected = IS.format("name", "Departing Employee")
    assert str(_filter) == expected


def test_rule_name_not_eq_str_gives_correct_json_representation():
    _filter = RuleName.not_eq("Departing Employee")
    expected = IS_NOT.format("name", "Departing Employee")
    assert str(_filter) == expected


def test_rule_name_is_in_str_gives_correct_json_representation():
    items = ["rule 1", "rule 2", "rule 3"]
    _filter = RuleName.is_in(items)
    expected = IS_IN.format("name", *sorted(items))
    assert str(_filter) == expected


def test_rule_name_not_in_str_gives_correct_json_representation():
    items = ["rule 1", "rule 2", "rule 3"]
    _filter = RuleName.not_in(items)
    expected = NOT_IN.format("name", *sorted(items))
    assert str(_filter) == expected


def test_rule_name_contains_str_gives_correct_json_representation():
    _filter = RuleName.contains("test")
    expected = CONTAINS.format("name", "test")
    assert str(_filter) == expected


def test_rule_name_not_contains_str_gives_correct_json_representation():
    _filter = RuleName.not_contains("test")
    expected = NOT_CONTAINS.format("name", "test")
    assert str(_filter) == expected


def test_rule_id_eq_str_gives_correct_json_representation():
    _filter = RuleId.eq("rule123")
    expected = IS.format("ruleId", "rule123")
    assert str(_filter) == expected


def test_rule_id_not_eq_str_gives_correct_json_representation():
    _filter = RuleId.not_eq("rule123")
    expected = IS_NOT.format("ruleId", "rule123")
    assert str(_filter) == expected


def test_rule_id_is_in_str_gives_correct_json_representation():
    items = ["rule1", "rule2", "rule3"]
    _filter = RuleId.is_in(items)
    expected = IS_IN.format("ruleId", *sorted(items))
    assert str(_filter) == expected


def test_rule_id_not_in_str_gives_correct_json_representation():
    items = ["rule 1", "rule 2", "rule 3"]
    _filter = RuleId.not_in(items)
    expected = NOT_IN.format("ruleId", *sorted(items))
    assert str(_filter) == expected


def test_rule_type_eq_str_gives_correct_json_representation():
    _filter = RuleType.eq("rule123")
    expected = IS.format("type", "rule123")
    assert str(_filter) == expected


def test_rule_type_not_eq_str_gives_correct_json_representation():
    _filter = RuleType.not_eq("rule123")
    expected = IS_NOT.format("type", "rule123")
    assert str(_filter) == expected


def test_rule_type_is_in_str_gives_correct_json_representation():
    items = ["rule1", "rule2", "rule3"]
    _filter = RuleType.is_in(items)
    expected = IS_IN.format("type", *sorted(items))
    assert str(_filter) == expected


def test_rule_type_not_in_str_gives_correct_json_representation():
    items = ["rule 1", "rule 2", "rule 3"]
    _filter = RuleType.not_in(items)
    expected = NOT_IN.format("type", *sorted(items))
    assert str(_filter) == expected


def test_rule_source_eq_str_gives_correct_json_representation():
    _filter = RuleSource.eq("rule123")
    expected = IS.format("ruleSource", "rule123")
    assert str(_filter) == expected


def test_rule_source_not_eq_str_gives_correct_json_representation():
    _filter = RuleSource.not_eq("rule123")
    expected = IS_NOT.format("ruleSource", "rule123")
    assert str(_filter) == expected


def test_rule_source_is_in_str_gives_correct_json_representation():
    items = ["rule1", "rule2", "rule3"]
    _filter = RuleSource.is_in(items)
    expected = IS_IN.format("ruleSource", *sorted(items))
    assert str(_filter) == expected


def test_rule_source_not_in_str_gives_correct_json_representation():
    items = ["rule 1", "rule 2", "rule 3"]
    _filter = RuleSource.not_in(items)
    expected = NOT_IN.format("ruleSource", *sorted(items))
    assert str(_filter) == expected


def test_description_eq_str_gives_correct_json_representation():
    _filter = Description.eq("Departing Employee")
    expected = IS.format("description", "Departing Employee")
    assert str(_filter) == expected


def test_description_not_eq_str_gives_correct_json_representation():
    _filter = Description.not_eq("Departing Employee")
    expected = IS_NOT.format("description", "Departing Employee")
    assert str(_filter) == expected


def test_description_is_in_str_gives_correct_json_representation():
    items = ["desc1", "desc2", "desc3"]
    _filter = Description.is_in(items)
    expected = IS_IN.format("description", *sorted(items))
    assert str(_filter) == expected


def test_description_not_in_str_gives_correct_json_representation():
    items = ["desc1", "desc2", "desc3"]
    _filter = Description.not_in(items)
    expected = NOT_IN.format("description", *sorted(items))
    assert str(_filter) == expected


def test_description_contains_str_gives_correct_json_representation():
    _filter = Description.contains("test")
    expected = CONTAINS.format("description", "test")
    assert str(_filter) == expected


def test_description_not_contains_str_gives_correct_json_representation():
    _filter = Description.not_contains("test")
    expected = NOT_CONTAINS.format("description", "test")
    assert str(_filter) == expected


def test_alert_state_eq_str_gives_correct_json_representation():
    _filter = AlertState.eq("OPEN")
    expected = IS.format("state", "OPEN")
    assert str(_filter) == expected


def test_alert_state_not_eq_str_gives_correct_json_representation():
    _filter = AlertState.not_eq("OPEN")
    expected = IS_NOT.format("state", "OPEN")
    assert str(_filter) == expected


def test_alert_state_is_in_str_gives_correct_json_representation():
    items = ["OPEN", "DISMISSED", "OTHER"]
    _filter = AlertState.is_in(items)
    expected = IS_IN.format("state", *sorted(items))
    assert str(_filter) == expected


def test_alert_state_not_in_str_gives_correct_json_representation():
    items = ["OPEN", "DISMISSED", "other"]
    _filter = AlertState.not_in(items)
    expected = NOT_IN.format("state", *sorted(items))
    assert str(_filter) == expected


def test_rule_source_choices_returns_set():
    choices = RuleSource.choices()
    valid_set = {"Alerting", "Departing Employee", "High Risk Employee"}
    assert set(choices) == valid_set


def test_rule_type_choices_returns_set():
    choices = RuleType.choices()
    valid_set = {
        "FedEndpointExfiltration",
        "FedCloudSharePermissions",
        "FedFileTypeMismatch",
    }
    assert set(choices) == valid_set


def test_severity_choices_returns_set():
    choices = Severity.choices()
    valid_set = {"HIGH", "MEDIUM", "LOW"}
    assert set(choices) == valid_set


def test_alert_state_choices_returns_set():
    choices = AlertState.choices()
    valid_set = {"OPEN", "RESOLVED"}
    assert set(choices) == valid_set

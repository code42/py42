from datetime import datetime

import pytest

from py42.sdk.queries.query_filter import _QueryFilter
from py42.sdk.queries.query_filter import _QueryFilterTimestampField
from py42.sdk.queries.query_filter import create_eq_filter_group
from py42.sdk.queries.query_filter import create_filter_group
from py42.sdk.queries.query_filter import create_in_range_filter_group
from py42.sdk.queries.query_filter import create_is_in_filter_group
from py42.sdk.queries.query_filter import create_not_eq_filter_group
from py42.sdk.queries.query_filter import create_not_in_filter_group
from py42.sdk.queries.query_filter import create_on_or_after_filter_group
from py42.sdk.queries.query_filter import create_on_or_before_filter_group
from py42.sdk.queries.query_filter import create_query_filter
from py42.sdk.queries.query_filter import FilterGroup


EVENT_FILTER_FIELD_NAME = "filter_field_name"
OPERATOR_STRING = "IS_IN"
VALUE_STRING = "value_example"
VALUE_UNICODE = "您已经发现了秘密信息"
TEST_TIMESTAMP = "2020-09-10 11:12:13"

JSON_QUERY_FILTER = f'{{"operator":"{OPERATOR_STRING}", "term":"{EVENT_FILTER_FIELD_NAME}", "value":"{VALUE_STRING}"}}'

JSON_FILTER_GROUP_BASE = '{{"filterClause":"{0}", "filters":[{1}]}}'
JSON_FILTER_GROUP_AND = JSON_FILTER_GROUP_BASE.format("AND", JSON_QUERY_FILTER)
JSON_FILTER_GROUP_OR = JSON_FILTER_GROUP_BASE.format("OR", JSON_QUERY_FILTER)


def json_query_filter_with_suffix(suffix):
    return f'{{"operator":"{OPERATOR_STRING}{suffix}", "term":"{EVENT_FILTER_FIELD_NAME}{suffix}", "value":"{VALUE_STRING}{suffix}"}}'


def test_query_filter_constructs_successfully():
    assert _QueryFilter(EVENT_FILTER_FIELD_NAME, OPERATOR_STRING, VALUE_STRING)


def test_query_filter_str_outputs_correct_json_representation(query_filter):
    assert str(query_filter) == JSON_QUERY_FILTER


def test_query_filter_unicode_outputs_correct_json_representation(unicode_query_filter):
    expected = f'{{"operator":"{OPERATOR_STRING}", "term":"{EVENT_FILTER_FIELD_NAME}", "value":"{VALUE_UNICODE}"}}'
    assert str(unicode_query_filter) == expected


def test_query_filter_from_dict_gives_correct_json_representation():
    filter_dict = {"operator": "IS", "term": "testterm", "value": "testval"}
    filter_json = '{"operator":"IS", "term":"testterm", "value":"testval"}'
    alert_query = _QueryFilter.from_dict(filter_dict)
    assert str(alert_query) == filter_json


def test_query_filter_dict_gives_expected_dict_representation(event_filter_group):
    query_filter = _QueryFilter("testterm", "IS", value="testval")
    alert_query_query_dict = dict(query_filter)
    assert alert_query_query_dict["term"] == "testterm"
    assert alert_query_query_dict["operator"] == "IS"
    assert alert_query_query_dict["value"] == "testval"


def test_query_filter_term_returns_expected_value():
    query_filter = _QueryFilter("testterm", "IS", value="testval")
    assert query_filter.term == "testterm"


def test_query_filter_operator_returns_expected_value():
    query_filter = _QueryFilter("testterm", "IS", value="testval")
    assert query_filter.operator == "IS"


def test_query_filter_value_returns_expected_value():
    query_filter = _QueryFilter("testterm", "IS", value="testval")
    assert query_filter.value == "testval"


def test_filter_group_constructs_successfully(query_filter):
    assert create_filter_group(query_filter, "AND")


def test_filter_group_str_gives_correct_json_representation(query_filter):
    assert str(create_filter_group([query_filter], "AND")) == JSON_FILTER_GROUP_AND


def test_filter_group_with_and_specified_str_gives_correct_json_representation(
    query_filter,
):
    assert str(create_filter_group([query_filter], "AND")) == JSON_FILTER_GROUP_AND


def test_filter_group_with_or_specified_str_gives_correct_json_representation(
    query_filter,
):
    assert str(create_filter_group([query_filter], "OR")) == JSON_FILTER_GROUP_OR


def test_filter_group_from_dict_gives_correct_json_representation(query_filter):
    filter_group_dict = {
        "filterClause": "AND",
        "filters": [{"operator": "IS", "term": "testterm", "value": "testval"}],
    }
    expected = '{"filterClause":"AND", "filters":[{"operator":"IS", "term":"testterm", "value":"testval"}]}'
    filter_group = FilterGroup.from_dict(filter_group_dict)
    assert str(filter_group) == expected


def test_filter_group_dict_gives_expected_dict_representation(query_filter):
    filter_group = create_filter_group([query_filter], "AND")
    filter_group_dict = dict(filter_group)
    assert filter_group_dict["filterClause"] == "AND"
    assert type(filter_group_dict["filters"]) == list


def test_filter_group_filter_list_returns_expected_value(query_filter):
    filter_list = [query_filter]
    filter_group = create_filter_group(filter_list, "AND")
    assert filter_group.filter_list == filter_list


def test_filter_group_filter_clause_returns_excepted_value(query_filter):
    filter_group = create_filter_group([query_filter], "AND")
    assert filter_group.filter_clause == "AND"


def test_filter_group_with_multiple_filters_str_gives_correct_json_representation(
    query_filter_list,
):
    filters_string = ",".join(
        [json_query_filter_with_suffix(suffix) for suffix in range(3)]
    )
    json_multi_filter_group = JSON_FILTER_GROUP_BASE.format("AND", filters_string)
    assert str(create_filter_group(query_filter_list, "AND")) == json_multi_filter_group


def test_filter_group_with_multiple_filters_and_specified_str_gives_correct_json_representation(
    query_filter_list,
):
    filters_string = ",".join(
        [json_query_filter_with_suffix(suffix) for suffix in range(3)]
    )
    json_multi_filter_group = JSON_FILTER_GROUP_BASE.format("AND", filters_string)
    assert str(create_filter_group(query_filter_list, "AND")) == json_multi_filter_group


def test_filter_group_with_duplicate_filters_and_specified_str_gives_correct_json_representation(
    query_filter,
):
    expected = JSON_FILTER_GROUP_BASE.format("AND", JSON_QUERY_FILTER)
    assert (
        str(create_filter_group([query_filter, query_filter, query_filter], "AND"))
        == expected
    )


def test_filter_group_with_multiple_filters_or_specified_str_gives_correct_json_representation(
    query_filter_list,
):
    filters_string = ",".join(
        [json_query_filter_with_suffix(suffix) for suffix in range(3)]
    )
    json_multi_filter_group = JSON_FILTER_GROUP_BASE.format("OR", filters_string)
    assert str(create_filter_group(query_filter_list, "OR")) == json_multi_filter_group


def test_filter_group_with_duplicate_filters_or_specified_str_gives_correct_json_representation(
    query_filter,
):
    expected = JSON_FILTER_GROUP_BASE.format("OR", JSON_QUERY_FILTER)
    assert (
        str(create_filter_group([query_filter, query_filter, query_filter], "OR"))
        == expected
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
    filter_group = create_in_range_filter_group(
        "rangeterm", "beforevalue", "aftervalue"
    )
    assert (
        str(filter_group) == '{"filterClause":"AND",'
        ' "filters":[{"operator":"ON_OR_AFTER", "term":"rangeterm", "value":"beforevalue"},'
        '{"operator":"ON_OR_BEFORE", "term":"rangeterm", "value":"aftervalue"}]}'
    )


def test_create_query_filter_returns_obj_with_correct_json_representation():
    query_filter = create_query_filter(
        EVENT_FILTER_FIELD_NAME, OPERATOR_STRING, VALUE_STRING
    )
    assert (
        str(query_filter)
        == f'{{"operator":"{OPERATOR_STRING}", "term":"{EVENT_FILTER_FIELD_NAME}", "value":"{VALUE_STRING}"}}'
    )


def test_compare_query_filters_with_equivalent_args_returns_true():
    query_filter1 = _QueryFilter(EVENT_FILTER_FIELD_NAME, OPERATOR_STRING, VALUE_STRING)
    query_filter2 = _QueryFilter(EVENT_FILTER_FIELD_NAME, OPERATOR_STRING, VALUE_STRING)
    assert query_filter1 == query_filter2


def test_compare_query_filters_with_different_values_returns_false():
    query_filter1 = _QueryFilter(EVENT_FILTER_FIELD_NAME, OPERATOR_STRING, "TEST")
    query_filter2 = _QueryFilter(EVENT_FILTER_FIELD_NAME, OPERATOR_STRING, "NOT_TEST")
    assert query_filter1 != query_filter2


def test_compare_query_filters_with_different_operators_returns_false():
    query_filter1 = _QueryFilter(EVENT_FILTER_FIELD_NAME, "IS", VALUE_STRING)
    query_filter2 = _QueryFilter(EVENT_FILTER_FIELD_NAME, "IS_NOT", VALUE_STRING)
    assert query_filter1 != query_filter2


def test_compare_query_filters_with_different_terms_returns_false():
    query_filter1 = _QueryFilter("TEST", OPERATOR_STRING, VALUE_STRING)
    query_filter2 = _QueryFilter("NOT_TEST", OPERATOR_STRING, VALUE_STRING)
    assert query_filter1 != query_filter2


@pytest.mark.parametrize(
    "equivalent",
    [
        f'{{"operator":"{OPERATOR_STRING}", "term":"{EVENT_FILTER_FIELD_NAME}", "value":"{VALUE_STRING}"}}',
        (
            ("operator", OPERATOR_STRING),
            ("term", EVENT_FILTER_FIELD_NAME),
            ("value", VALUE_STRING),
        ),
        [
            ("operator", OPERATOR_STRING),
            ("term", EVENT_FILTER_FIELD_NAME),
            ("value", VALUE_STRING),
        ],
    ],
)
def test_compare_query_filter_with_expected_equivalent_returns_true(equivalent):
    query_filter = _QueryFilter(EVENT_FILTER_FIELD_NAME, OPERATOR_STRING, VALUE_STRING)
    assert query_filter == equivalent


@pytest.mark.parametrize(
    "different",
    [
        f'{{"operator":"DIFFERENT_OPERATOR", "term":"{EVENT_FILTER_FIELD_NAME}", "value":"{VALUE_STRING}"}}',
        f'{{"operator":"{OPERATOR_STRING}", "term":"DIFFERENT_FIELD_NAME", "value":"{VALUE_STRING}"}}',
        f'{{"operator":"{OPERATOR_STRING}", "term":"{EVENT_FILTER_FIELD_NAME}", "value":"DIFFERENT_VALUE"}}',
        (
            ("operator", "DIFFERENT_OPERATOR"),
            ("term", EVENT_FILTER_FIELD_NAME),
            ("value", VALUE_STRING),
        ),
        (
            ("operator", OPERATOR_STRING),
            ("term", "DIFFERENT_FIELD_NAME"),
            ("value", VALUE_STRING),
        ),
        (
            ("operator", OPERATOR_STRING),
            ("term", EVENT_FILTER_FIELD_NAME),
            ("value", "DIFFERENT_VALUE"),
        ),
        [
            ("operator", "DIFFERENT_OPERATOR"),
            ("term", EVENT_FILTER_FIELD_NAME),
            ("value", VALUE_STRING),
        ],
        [
            ("operator", OPERATOR_STRING),
            ("term", "DIFFERENT_FIELD_NAME"),
            ("value", VALUE_STRING),
        ],
        [
            ("operator", OPERATOR_STRING),
            ("term", EVENT_FILTER_FIELD_NAME),
            ("value", "DIFFERENT_VALUE"),
        ],
    ],
)
def test_compare_query_filter_with_expected_different_returns_false(different):
    query_filter = _QueryFilter(EVENT_FILTER_FIELD_NAME, OPERATOR_STRING, VALUE_STRING)
    assert query_filter != different


def test_compare_filter_group_with_equivalent_single_args_return_true():
    group1 = create_eq_filter_group("eqterm", "eqvalue")
    group2 = create_eq_filter_group("eqterm", "eqvalue")
    assert group1 == group2


def test_compare_filter_group_with_equivalent_multiple_args_in_different_order_returns_true():
    group1 = create_is_in_filter_group("term", ["value1", "value2", "value3"])
    group2 = create_is_in_filter_group("term", ["value3", "value1", "value2"])
    assert group1 == group2
    assert str(group1) == group2
    assert tuple(group1) == group2
    assert list(group1) == group2
    assert group1 == str(group2)
    assert group1 == tuple(group2)
    assert group1 == list(group2)


@pytest.mark.parametrize(
    "filter_class",
    [
        _QueryFilter("term", "IS", "value1"),
        _QueryFilter("term", "IS", "value2"),
        _QueryFilter("term", "IS", "value3"),
    ],
)
def test_filter_group_contains_expected_query_filter_returns_true(filter_class):
    group = create_is_in_filter_group("term", ["value1", "value2", "value3"])
    assert filter_class in group
    assert str(filter_class) in group
    assert tuple(filter_class) in group
    assert list(filter_class) in group


@pytest.mark.parametrize(
    "filter_class",
    [
        _QueryFilter("term", "IS", "value4"),
        _QueryFilter("different_term", "IS", "value2"),
        _QueryFilter("term", "DIFFERENT_OPERATOR", "value3"),
    ],
)
def test_filter_group_when_does_not_contain_expected_query_filter_returns_false(
    filter_class,
):
    group = create_is_in_filter_group("term", ["value1", "value2", "value3"])
    assert filter_class not in group
    assert str(filter_class) not in group
    assert tuple(filter_class) not in group
    assert list(filter_class) not in group


def test_filter_group_when_changed_filter_clause_has_correct_json_representation():
    group = create_is_in_filter_group("term", ["value1", "value2", "value3"])
    assert (
        str(group) == '{"filterClause":"OR", "filters"'
        ':[{"operator":"IS", "term":"term", "value":"value1"},'
        '{"operator":"IS", "term":"term", "value":"value2"},'
        '{"operator":"IS", "term":"term", "value":"value3"}]}'
    )
    group.filter_clause = "AND"
    assert (
        str(group) == '{"filterClause":"AND", "filters"'
        ':[{"operator":"IS", "term":"term", "value":"value1"},'
        '{"operator":"IS", "term":"term", "value":"value2"},'
        '{"operator":"IS", "term":"term", "value":"value3"}]}'
    )


class Test_QueryFilterTimestampField:
    @pytest.mark.parametrize(
        "timestamp",
        [
            (TEST_TIMESTAMP),
            (1599736333.0),
            (1599736333),
            datetime.strptime(TEST_TIMESTAMP, "%Y-%m-%d %H:%M:%S"),
        ],
    )
    def test_on_or_after(self, timestamp):
        expected = {
            "filterClause": "AND",
            "filters": [
                {
                    "operator": "ON_OR_AFTER",
                    "term": "override_timestamp_field_name",
                    "value": "2020-09-10T11:12:13.000Z",
                }
            ],
        }

        qf = _QueryFilterTimestampField.on_or_after(timestamp)
        assert dict(qf) == expected

    @pytest.mark.parametrize(
        "timestamp",
        [
            (TEST_TIMESTAMP),
            (1599736333.0),
            (1599736333),
            datetime.strptime(TEST_TIMESTAMP, "%Y-%m-%d %H:%M:%S"),
        ],
    )
    def test_on_or_before(self, timestamp):
        expected = {
            "filterClause": "AND",
            "filters": [
                {
                    "operator": "ON_OR_BEFORE",
                    "term": "override_timestamp_field_name",
                    "value": "2020-09-10T11:12:13.000Z",
                }
            ],
        }
        assert dict(_QueryFilterTimestampField.on_or_before(timestamp)) == expected

    @pytest.mark.parametrize(
        "start_timestamp, end_timestamp",
        [
            (TEST_TIMESTAMP, "2020-09-10 12:13:14"),
            (1599736333.0, 1599739994.0),
            (1599736333, 1599739994),
            (
                datetime.strptime(TEST_TIMESTAMP, "%Y-%m-%d %H:%M:%S"),
                datetime.strptime("2020-09-10 12:13:14", "%Y-%m-%d %H:%M:%S"),
            ),
        ],
    )
    def test_in_range(self, start_timestamp, end_timestamp):
        expected = {
            "filterClause": "AND",
            "filters": [
                {
                    "operator": "ON_OR_AFTER",
                    "term": "override_timestamp_field_name",
                    "value": "2020-09-10T11:12:13.000Z",
                },
                {
                    "operator": "ON_OR_BEFORE",
                    "term": "override_timestamp_field_name",
                    "value": "2020-09-10T12:13:14.000Z",
                },
            ],
        }

        assert (
            dict(_QueryFilterTimestampField.in_range(start_timestamp, end_timestamp))
            == expected
        )

    @pytest.mark.parametrize(
        "timestamp",
        [
            (TEST_TIMESTAMP),
            (1599736333.0),
            (1599736333),
            datetime.strptime(TEST_TIMESTAMP, "%Y-%m-%d %H:%M:%S"),
        ],
    )
    def test_on_same_day(self, timestamp):
        expected = {
            "filterClause": "AND",
            "filters": [
                {
                    "operator": "ON_OR_AFTER",
                    "term": "override_timestamp_field_name",
                    "value": "2020-09-10T00:00:00.000Z",
                },
                {
                    "operator": "ON_OR_BEFORE",
                    "term": "override_timestamp_field_name",
                    "value": "2020-09-10T23:59:59.000Z",
                },
            ],
        }
        assert dict(_QueryFilterTimestampField.on_same_day(timestamp)) == expected

    def test_on_or_after_with_decimals(self):
        expected = {
            "filterClause": "AND",
            "filters": [
                {
                    "operator": "ON_OR_AFTER",
                    "term": "override_timestamp_field_name",
                    "value": "2020-09-10T11:12:13.123Z",
                }
            ],
        }

        qf = _QueryFilterTimestampField.on_or_after(1599736333.123456)
        assert dict(qf) == expected

    def test_on_or_before_with_decimals(self):
        expected = {
            "filterClause": "AND",
            "filters": [
                {
                    "operator": "ON_OR_BEFORE",
                    "term": "override_timestamp_field_name",
                    "value": "2020-09-10T11:12:13.123Z",
                }
            ],
        }
        assert (
            dict(_QueryFilterTimestampField.on_or_before(1599736333.123456)) == expected
        )

    def test_in_range_with_decimals(self):
        expected = {
            "filterClause": "AND",
            "filters": [
                {
                    "operator": "ON_OR_AFTER",
                    "term": "override_timestamp_field_name",
                    "value": "2020-09-10T11:12:13.123Z",
                },
                {
                    "operator": "ON_OR_BEFORE",
                    "term": "override_timestamp_field_name",
                    "value": "2020-09-10T12:13:14.678Z",
                },
            ],
        }

        assert (
            dict(
                _QueryFilterTimestampField.in_range(1599736333.123456, 1599739994.6789)
            )
            == expected
        )

import pytest
from py42._internal.file_event_filter import FileEventFilter, FilterGroup, create_filter_group


EVENT_FILTER_FIELD_NAME = "filter_field_name"
OPERATOR_STRING = "IS_IN"
VALUE_STRING = "value_example"

JSON_FILE_EVENT_FILTER = '{{"operator":"{0}", "term":"{1}", "value":"{2}"}}'.format(
                                                                          OPERATOR_STRING,
                                                                          EVENT_FILTER_FIELD_NAME,
                                                                          VALUE_STRING)

JSON_FILTER_GROUP_BASE = '{{"filterClause":"{0}", "filters":[{1}]}}'
JSON_FILTER_GROUP_AND = JSON_FILTER_GROUP_BASE.format("AND", JSON_FILE_EVENT_FILTER)
JSON_FILTER_GROUP_OR = JSON_FILTER_GROUP_BASE.format("OR", JSON_FILE_EVENT_FILTER)


@pytest.fixture
def file_event_filter():
    return FileEventFilter(EVENT_FILTER_FIELD_NAME, OPERATOR_STRING, VALUE_STRING)


@pytest.fixture
def file_event_filter_list(file_event_filter):
    return [file_event_filter for _ in range(3)]


@pytest.fixture
def event_filter_group(file_event_filter):
    return FilterGroup([file_event_filter])


@pytest.fixture
def event_filter_group_list(event_filter_group):
    return [event_filter_group for _ in range(3)]


def test_file_event_filter_constructs_successfully():
    assert FileEventFilter(EVENT_FILTER_FIELD_NAME, OPERATOR_STRING, VALUE_STRING)


def test_file_event_filter_str_outputs_correct_json_representation(file_event_filter):
    assert str(file_event_filter) == JSON_FILE_EVENT_FILTER


def test_filter_group_constructs_successfully(file_event_filter):
    assert create_filter_group(file_event_filter)


def test_filter_group_str_gives_correct_json_representation(file_event_filter):
    assert str(create_filter_group([file_event_filter])) == JSON_FILTER_GROUP_AND


def test_filter_group_with_and_specified_str_gives_correct_json_representation(file_event_filter):
    assert str(create_filter_group([file_event_filter], "AND")) == JSON_FILTER_GROUP_AND


def test_filter_group_with_or_specified_str_gives_correct_json_representation(file_event_filter):
    assert str(create_filter_group([file_event_filter], "OR")) == JSON_FILTER_GROUP_OR


def test_filter_group_with_multiple_filters_str_gives_correct_json_representation(file_event_filter_list):
    filters_string = ",".join([JSON_FILE_EVENT_FILTER for _ in range(3)])
    json_multi_filter_group = JSON_FILTER_GROUP_BASE.format("AND", filters_string)
    assert str(create_filter_group(file_event_filter_list)) == json_multi_filter_group


def test_filter_group_with_multiple_filters_and_specified_str_gives_correct_json_representation(file_event_filter_list):
    filters_string = ",".join([JSON_FILE_EVENT_FILTER for _ in range(3)])
    json_multi_filter_group = JSON_FILTER_GROUP_BASE.format("AND", filters_string)
    assert str(create_filter_group(file_event_filter_list, "AND")) == json_multi_filter_group


def test_filter_group_with_multiple_filters_or_specified_str_gives_correct_json_representation(file_event_filter_list):
    filters_string = ",".join([JSON_FILE_EVENT_FILTER for _ in range(3)])
    json_multi_filter_group = JSON_FILTER_GROUP_BASE.format("OR", filters_string)
    assert str(create_filter_group(file_event_filter_list, "OR")) == json_multi_filter_group
# -*- coding: utf-8 -*-

import pytest
from datetime import datetime

from py42._internal.filters.query_filter import QueryFilter, FilterGroup

EVENT_FILTER_FIELD_NAME = "filter_field_name"
OPERATOR_STRING = "IS_IN"
VALUE_STRING = "value_example"
VALUE_UNICODE = u"您已经发现了秘密信息"


@pytest.fixture
def event_filter_group(query_filter):
    return FilterGroup([query_filter])


@pytest.fixture
def unicode_event_filter_group(unicode_query_filter):
    return FilterGroup([unicode_query_filter])


@pytest.fixture
def event_filter_group_list(event_filter_group):
    return [event_filter_group for _ in range(3)]


@pytest.fixture
def query_filter():
    return QueryFilter(EVENT_FILTER_FIELD_NAME, OPERATOR_STRING, VALUE_STRING)


@pytest.fixture
def unicode_query_filter():
    return QueryFilter(EVENT_FILTER_FIELD_NAME, OPERATOR_STRING, VALUE_UNICODE)


@pytest.fixture
def exists_filter_creator(mocker):
    return mocker.patch(create_file_event_filter_creator_path("exists"))


@pytest.fixture
def not_exists_filter_creator(mocker):
    return mocker.patch(create_file_event_filter_creator_path("not_exists"))


@pytest.fixture
def eq_filter_creator(mocker):
    return mocker.patch(create_base_filter_creator_path("eq"))


@pytest.fixture
def not_eq_filter_creator(mocker):
    return mocker.patch(create_base_filter_creator_path("not_eq"))


@pytest.fixture
def contains_filter_creator(mocker):
    return mocker.patch(create_alert_filter_creator_path("contains"))


@pytest.fixture
def not_contains_filter_creator(mocker):
    return mocker.patch(create_alert_filter_creator_path("not_contains"))


@pytest.fixture
def is_in_filter_creator(mocker):
    return mocker.patch(create_base_filter_creator_path("is_in"))


@pytest.fixture
def not_in_filter_creator(mocker):
    return mocker.patch(create_base_filter_creator_path("not_in"))


@pytest.fixture
def on_or_after_filter_creator(mocker):
    return mocker.patch(create_base_filter_creator_path("on_or_after"))


@pytest.fixture
def on_or_before_filter_creator(mocker):
    return mocker.patch(create_base_filter_creator_path("on_or_before"))


@pytest.fixture
def in_range_filter_creator(mocker):
    return mocker.patch(create_base_filter_creator_path("in_range"))


def create_base_filter_creator_path(query_filter_string):
    return "py42._internal.filters.query_filter.create_{0}_filter_group".format(query_filter_string)


def create_file_event_filter_creator_path(query_filter_string):
    return "py42._internal.filters.file_event_filter.create_{0}_filter_group".format(
        query_filter_string
    )


def create_alert_filter_creator_path(query_filter_string):
    return "py42._internal.filters.alert_filter.create_{0}_filter_group".format(query_filter_string)


def format_timestamp(test_time):
    test_date = datetime.utcfromtimestamp(test_time)
    return format_datetime(test_date)


def format_datetime(test_date):
    prefix = test_date.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
    timestamp_str = "{0}Z".format(prefix)
    return timestamp_str

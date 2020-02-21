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


def format_timestamp(test_time):
    test_date = datetime.utcfromtimestamp(test_time)
    return format_datetime(test_date)


def format_datetime(test_date):
    prefix = test_date.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
    timestamp_str = "{0}Z".format(prefix)
    return timestamp_str

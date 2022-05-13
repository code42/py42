from datetime import datetime

import pytest

from py42.sdk.queries.query_filter import FilterGroup
from py42.sdk.queries.query_filter import QueryFilter
from py42.util import MICROSECOND_FORMAT

EVENT_FILTER_FIELD_NAME = "filter_field_name"
OPERATOR_STRING = "IS_IN"
VALUE_STRING = "value_example"
VALUE_UNICODE = "您已经发现了秘密信息"

EXISTS = '{{"filterClause":"AND", "filters":[{{"operator":"EXISTS", "term":"{0}", "value":null}}]}}'
NOT_EXISTS = '{{"filterClause":"AND", "filters":[{{"operator":"DOES_NOT_EXIST", "term":"{0}", "value":null}}]}}'
IS = '{{"filterClause":"AND", "filters":[{{"operator":"IS", "term":"{0}", "value":"{1}"}}]}}'
IS_NOT = '{{"filterClause":"AND", "filters":[{{"operator":"IS_NOT", "term":"{0}", "value":"{1}"}}]}}'
IS_IN = '{{"filterClause":"OR", "filters":[{{"operator":"IS", "term":"{0}", "value":"{1}"}},{{"operator":"IS", "term":"{0}", "value":"{2}"}},{{"operator":"IS", "term":"{0}", "value":"{3}"}}]}}'
NOT_IN = '{{"filterClause":"AND", "filters":[{{"operator":"IS_NOT", "term":"{0}", "value":"{1}"}},{{"operator":"IS_NOT", "term":"{0}", "value":"{2}"}},{{"operator":"IS_NOT", "term":"{0}", "value":"{3}"}}]}}'
IN_RANGE = '{{"filterClause":"AND", "filters":[{{"operator":"ON_OR_AFTER", "term":"{0}", "value":"{1}"}},{{"operator":"ON_OR_BEFORE", "term":"{0}", "value":"{2}"}}]}}'

ON_OR_AFTER = '{{"filterClause":"AND", "filters":[{{"operator":"ON_OR_AFTER", "term":"{0}", "value":"{1}"}}]}}'
ON_OR_BEFORE = '{{"filterClause":"AND", "filters":[{{"operator":"ON_OR_BEFORE", "term":"{0}", "value":"{1}"}}]}}'

CONTAINS = '{{"filterClause":"AND", "filters":[{{"operator":"CONTAINS", "term":"{0}", "value":"{1}"}}]}}'
NOT_CONTAINS = '{{"filterClause":"AND", "filters":[{{"operator":"DOES_NOT_CONTAIN", "term":"{0}", "value":"{1}"}}]}}'

GREATER_THAN = '{{"filterClause":"AND", "filters":[{{"operator":"GREATER_THAN", "term":"{0}", "value":"{1}"}}]}}'
LESS_THAN = '{{"filterClause":"AND", "filters":[{{"operator":"LESS_THAN", "term":"{0}", "value":"{1}"}}]}}'
WITHIN_THE_LAST = '{{"filterClause":"AND", "filters":[{{"operator":"WITHIN_THE_LAST", "term":"{0}", "value":"{1}"}}]}}'


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
    prefix = test_date.strftime(MICROSECOND_FORMAT)[:-4]
    timestamp_str = f"{prefix}Z"
    return timestamp_str

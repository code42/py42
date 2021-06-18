# -*- coding: utf-8 -*-
from datetime import datetime

import pytest

from py42.sdk.queries.query_filter import FilterGroup
from py42.sdk.queries.query_filter import QueryFilter
from py42.util import MILLISECOND_FORMAT

EVENT_FILTER_FIELD_NAME = "filter_field_name"
OPERATOR_STRING = "IS_IN"
VALUE_STRING = "value_example"
VALUE_UNICODE = u"您已经发现了秘密信息"

EXISTS = u'{{"filterClause":"AND", "filters":[{{"operator":"EXISTS", "term":"{0}", "value":null}}]}}'
NOT_EXISTS = u'{{"filterClause":"AND", "filters":[{{"operator":"DOES_NOT_EXIST", "term":"{0}", "value":null}}]}}'
IS = u'{{"filterClause":"AND", "filters":[{{"operator":"IS", "term":"{0}", "value":"{1}"}}]}}'
IS_NOT = u'{{"filterClause":"AND", "filters":[{{"operator":"IS_NOT", "term":"{0}", "value":"{1}"}}]}}'
IS_IN = u'{{"filterClause":"OR", "filters":[{{"operator":"IS", "term":"{0}", "value":"{1}"}},{{"operator":"IS", "term":"{0}", "value":"{2}"}},{{"operator":"IS", "term":"{0}", "value":"{3}"}}]}}'
NOT_IN = u'{{"filterClause":"AND", "filters":[{{"operator":"IS_NOT", "term":"{0}", "value":"{1}"}},{{"operator":"IS_NOT", "term":"{0}", "value":"{2}"}},{{"operator":"IS_NOT", "term":"{0}", "value":"{3}"}}]}}'
IN_RANGE = u'{{"filterClause":"AND", "filters":[{{"operator":"ON_OR_AFTER", "term":"{0}", "value":"{1}"}},{{"operator":"ON_OR_BEFORE", "term":"{0}", "value":"{2}"}}]}}'

ON_OR_AFTER = u'{{"filterClause":"AND", "filters":[{{"operator":"ON_OR_AFTER", "term":"{0}", "value":"{1}"}}]}}'
ON_OR_BEFORE = u'{{"filterClause":"AND", "filters":[{{"operator":"ON_OR_BEFORE", "term":"{0}", "value":"{1}"}}]}}'

CONTAINS = u'{{"filterClause":"AND", "filters":[{{"operator":"CONTAINS", "term":"{0}", "value":"{1}"}}]}}'
NOT_CONTAINS = u'{{"filterClause":"AND", "filters":[{{"operator":"DOES_NOT_CONTAIN", "term":"{0}", "value":"{1}"}}]}}'

GREATER_THAN = u'{{"filterClause":"AND", "filters":[{{"operator":"GREATER_THAN", "term":"{0}", "value":"{1}"}}]}}'
LESS_THAN = u'{{"filterClause":"AND", "filters":[{{"operator":"LESS_THAN", "term":"{0}", "value":"{1}"}}]}}'
WITHIN_THE_LAST = u'{{"filterClause":"AND", "filters":[{{"operator":"WITHIN_THE_LAST", "term":"{0}", "value":"{1}"}}]}}'


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
    prefix = test_date.strftime(MILLISECOND_FORMAT)[:-3]
    timestamp_str = "{}Z".format(prefix)
    return timestamp_str

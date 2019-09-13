# -*- coding: utf-8 -*-

import pytest

from py42._internal.file_event_filter import FileEventFilter, FilterGroup

EVENT_FILTER_FIELD_NAME = "filter_field_name"
OPERATOR_STRING = "IS_IN"
VALUE_STRING = "value_example"
VALUE_UNICODE = u"我能吞下玻璃而不伤身体"


@pytest.fixture
def event_filter_group(file_event_filter):
    return FilterGroup([file_event_filter])


@pytest.fixture
def unicode_event_filter_group(unicode_file_event_filter):
    return FilterGroup([unicode_file_event_filter])


@pytest.fixture
def event_filter_group_list(event_filter_group):
    return [event_filter_group for _ in range(3)]


@pytest.fixture
def file_event_filter():
    return FileEventFilter(EVENT_FILTER_FIELD_NAME, OPERATOR_STRING, VALUE_STRING)


@pytest.fixture
def unicode_file_event_filter():
    return FileEventFilter(EVENT_FILTER_FIELD_NAME, OPERATOR_STRING, VALUE_UNICODE)
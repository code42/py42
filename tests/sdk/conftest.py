# -*- coding: utf-8 -*-

import pytest

from py42._internal.file_event_filter import FileEventFilter, FilterGroup

EVENT_FILTER_FIELD_NAME = "filter_field_name"
OPERATOR_STRING = "IS_IN"
VALUE_STRING = "value_example"
VALUE_UNICODE = u"您已经发现了秘密信息"


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


@pytest.fixture
def exists_filter_creator(mocker):
    return mocker.patch(create_filter_creator_path("exists"))


@pytest.fixture
def not_exists_filter_creator(mocker):
    return mocker.patch(create_filter_creator_path("not_exists"))


@pytest.fixture
def eq_filter_creator(mocker):
    return mocker.patch(create_filter_creator_path("eq"))


@pytest.fixture
def not_eq_filter_creator(mocker):
    return mocker.patch(create_filter_creator_path("not_eq"))


@pytest.fixture
def is_in_filter_creator(mocker):
    return mocker.patch(create_filter_creator_path("is_in"))


@pytest.fixture
def not_in_filter_creator(mocker):
    return mocker.patch(create_filter_creator_path("not_in"))


@pytest.fixture
def on_or_after_filter_creator(mocker):
    return mocker.patch(create_filter_creator_path("on_or_after"))


@pytest.fixture
def on_or_before_filter_creator(mocker):
    return mocker.patch(create_filter_creator_path("on_or_before"))


@pytest.fixture
def in_range_filter_creator(mocker):
    return mocker.patch(create_filter_creator_path("in_range"))


def create_filter_creator_path(query_filter_string):
    return "py42._internal.file_event_filter.create_{0}_filter_group".format(query_filter_string)

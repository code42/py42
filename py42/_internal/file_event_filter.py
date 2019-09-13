# -*- coding: utf-8 -*-

from datetime import datetime


def create_file_event_filter(term, operator, value):
    return FileEventFilter(term, operator, value)


def create_eq_filter_group(term, value):
    filter_list = [create_file_event_filter(term, "IS", value)]
    return create_filter_group(filter_list, "AND")


def create_is_in_filter_group(term, value_list):
    filter_list = [create_file_event_filter(term, "IS", value) for value in value_list]
    return create_filter_group(filter_list, "OR" if len(filter_list) > 1 else "AND")


def create_not_in_filter_group(term, value_list):
    filter_list = [create_file_event_filter(term, "IS_NOT", value) for value in value_list]
    return create_filter_group(filter_list, "AND")


def create_not_eq_filter_group(term, value):
    filter_list = [create_file_event_filter(term, "IS_NOT", value)]
    return create_filter_group(filter_list, "AND")


def create_on_or_after_filter_group(term, value):
    filter_list = [create_file_event_filter(term, "ON_OR_AFTER", value)]
    return create_filter_group(filter_list, "AND")


def create_on_or_before_filter_group(term, value):
    filter_list = [create_file_event_filter(term, "ON_OR_BEFORE", value)]
    return create_filter_group(filter_list, "AND")


def create_in_range_filter_group(term, start_value, end_value):
    filter_list = [create_file_event_filter(term, "ON_OR_AFTER", start_value),
                   create_file_event_filter(term, "ON_OR_BEFORE", end_value)]
    return create_filter_group(filter_list, "AND")


def create_filter_group(file_event_filter_list, filter_clause):
    return FilterGroup(file_event_filter_list, filter_clause)


class _FileEventFilterStringField(object):
    _term = "override_string_field_name"

    @classmethod
    def eq(cls, value):
        # type: (str) -> FilterGroup
        return create_eq_filter_group(cls._term, value)

    @classmethod
    def not_eq(cls, value):
        # type: (str) -> FilterGroup
        return create_not_eq_filter_group(cls._term, value)

    @classmethod
    def is_in(cls, value_list):
        # type: (iter[str]) -> FilterGroup
        return create_is_in_filter_group(cls._term, value_list)

    @classmethod
    def not_in(cls, value_list):
        # type: (iter[str]) -> FilterGroup
        return create_not_in_filter_group(cls._term, value_list)


class _FileEventFilterTimestampField(object):
    _term = "override_timestamp_field_name"

    @staticmethod
    def _to_timestamp_string(int_value):
        # "2018-12-01T00:00:00.000Z"
        return datetime.fromtimestamp(int_value).strftime("%Y-%m-%dT%H:%M:%S.000Z")

    @classmethod
    def on_or_after(cls, value):
        formatted_timestamp = cls._to_timestamp_string(value)
        return create_on_or_after_filter_group(cls._term, formatted_timestamp)

    @classmethod
    def on_or_before(cls, value):
        formatted_timestamp = cls._to_timestamp_string(value)
        return create_on_or_before_filter_group(cls._term, formatted_timestamp)

    @classmethod
    def in_range(cls, start_value, end_value):
        formatted_start_time = cls._to_timestamp_string(start_value)
        formatted_end_time = cls._to_timestamp_string(end_value)
        return create_in_range_filter_group(cls._term, formatted_start_time, formatted_end_time)


class FileEventFilter(object):

    _term = None

    def __init__(self, term, operator, value):
        self._term = term
        self._operator = operator
        self._value = value

    def __unicode__(self):
        return u'{{"operator":"{0}", "term":"{1}", "value":"{2}"}}'.format(self._operator, self._term, self._value)

    def __repr__(self):
        return self.__unicode__().encode("utf-8")


class FilterGroup(object):
    def __init__(self, filter_list, filter_clause="AND"):
        self._filter_list = filter_list
        self._filter_clause = filter_clause

    def __unicode__(self):
        filters_string = ",".join(unicode(filter_item) for filter_item in self._filter_list)
        return u'{{"filterClause":"{0}", "filters":[{1}]}}'.format(self._filter_clause, filters_string)

    def __repr__(self):
        return self.__unicode__().encode("utf-8")

# -*- coding: utf-8 -*-

from datetime import datetime

from py42._internal.compat import str
from py42.util import convert_timestamp_to_str, convert_datetime_to_timestamp_str


def create_query_filter(term, operator, value=None):
    return QueryFilter(term, operator, value)


def create_eq_filter_group(term, value):
    filter_list = [create_query_filter(term, u"IS", value)]
    return create_filter_group(filter_list, u"AND")


def create_is_in_filter_group(term, value_list):
    filter_list = [create_query_filter(term, u"IS", value) for value in value_list]
    return create_filter_group(filter_list, u"OR" if len(filter_list) > 1 else u"AND")


def create_not_in_filter_group(term, value_list):
    filter_list = [create_query_filter(term, u"IS_NOT", value) for value in value_list]
    return create_filter_group(filter_list, u"AND")


def create_not_eq_filter_group(term, value):
    filter_list = [create_query_filter(term, u"IS_NOT", value)]
    return create_filter_group(filter_list, u"AND")


def create_on_or_after_filter_group(term, value):
    filter_list = [create_query_filter(term, u"ON_OR_AFTER", value)]
    return create_filter_group(filter_list, u"AND")


def create_on_or_before_filter_group(term, value):
    filter_list = [create_query_filter(term, u"ON_OR_BEFORE", value)]
    return create_filter_group(filter_list, u"AND")


def create_in_range_filter_group(term, start_value, end_value):
    filter_list = [
        create_query_filter(term, u"ON_OR_AFTER", start_value),
        create_query_filter(term, u"ON_OR_BEFORE", end_value),
    ]
    return create_filter_group(filter_list, u"AND")


def create_filter_group(query_filter_list, filter_clause):
    return FilterGroup(query_filter_list, filter_clause)


class _QueryFilterStringField(object):
    _term = u"override_string_field_name"

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


class _QueryFilterTimestampField(object):
    _term = u"override_timestamp_field_name"

    @classmethod
    def on_or_after(cls, value):
        formatted_timestamp = convert_timestamp_to_str(value)
        return create_on_or_after_filter_group(cls._term, formatted_timestamp)

    @classmethod
    def on_or_before(cls, value):
        formatted_timestamp = convert_timestamp_to_str(value)
        return create_on_or_before_filter_group(cls._term, formatted_timestamp)

    @classmethod
    def in_range(cls, start_value, end_value):
        formatted_start_time = convert_timestamp_to_str(start_value)
        formatted_end_time = convert_timestamp_to_str(end_value)
        return create_in_range_filter_group(cls._term, formatted_start_time, formatted_end_time)

    @classmethod
    def on_same_day(cls, value):
        date_from_value = datetime.utcfromtimestamp(value)
        start_time = datetime(
            date_from_value.year, date_from_value.month, date_from_value.day, 0, 0, 0
        )
        end_time = datetime(
            date_from_value.year, date_from_value.month, date_from_value.day, 23, 59, 59
        )
        formatted_start_time = convert_datetime_to_timestamp_str(start_time)
        formatted_end_time = convert_datetime_to_timestamp_str(end_time)
        return create_in_range_filter_group(cls._term, formatted_start_time, formatted_end_time)


class _QueryFilterBooleanField(object):
    _term = u"override_boolean_field_name"

    @classmethod
    def is_true(cls):
        return create_eq_filter_group(cls._term, u"TRUE")

    @classmethod
    def is_false(cls):
        return create_eq_filter_group(cls._term, u"FALSE")


class QueryFilter(object):
    _term = None

    def __init__(self, term, operator, value=None):
        self._term = term
        self._operator = operator
        self._value = value

    def __str__(self):
        value = u"null" if self._value is None else u'"{0}"'.format(self._value)
        return u'{{"operator":"{0}", "term":"{1}", "value":{2}}}'.format(
            self._operator, self._term, value
        )


class FilterGroup(object):
    def __init__(self, filter_list, filter_clause=u"AND"):
        self._filter_list = filter_list
        self._filter_clause = filter_clause

    def __str__(self):
        filters_string = u",".join(str(filter_item) for filter_item in self._filter_list)
        return u'{{"filterClause":"{0}", "filters":[{1}]}}'.format(
            self._filter_clause, filters_string
        )

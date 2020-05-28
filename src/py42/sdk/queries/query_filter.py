# -*- coding: utf-8 -*-

from datetime import datetime

from py42._internal.compat import str
from py42.util import convert_datetime_to_timestamp_str, convert_timestamp_to_str


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


class QueryFilterStringField(object):
    """Helper class for creating filters where the search value is a string."""

    _term = u"override_string_field_name"

    @classmethod
    def eq(cls, value):
        """Returns a :class:`FilterGroup` to find events where the filter equals the provided
        ``value``.

        Args:
            value (str): The value to match file events on.
        """
        return create_eq_filter_group(cls._term, value)

    @classmethod
    def not_eq(cls, value):
        """Returns a :class:`FilterGroup` to find events where the filter is not equal to the
        provided ``value``.

        Args:
            value (str): The value to exclude file events on.
        """
        return create_not_eq_filter_group(cls._term, value)

    @classmethod
    def is_in(cls, value_list):
        """Returns a :class:`FilterGroup` to find events where the filter is in the provided
        ``value_list``.

        Args:
            value_list (list): The list of values to match file events on.
        """
        return create_is_in_filter_group(cls._term, value_list)

    @classmethod
    def not_in(cls, value_list):
        """Returns a :class:`FilterGroup` to find events where the filter is not in the provided
        ``value_list``.

        Args:
            value_list (list): The list of values to exclude file events on.
        """
        return create_not_in_filter_group(cls._term, value_list)


class QueryFilterTimestampField(object):
    """Helper class for creating filters where the search value is a timestamp."""

    _term = u"override_timestamp_field_name"

    @classmethod
    def on_or_after(cls, value):
        """Returns a :class:`FilterGroup` to find events where the filter timestamp is on or after
        the provided `value`.
        """
        formatted_timestamp = convert_timestamp_to_str(value)
        return create_on_or_after_filter_group(cls._term, formatted_timestamp)

    @classmethod
    def on_or_before(cls, value):
        """Returns a :class:`FilterGroup` to find events where the filter timestamp is on or before
        the provided `value`.
        """
        formatted_timestamp = convert_timestamp_to_str(value)
        return create_on_or_before_filter_group(cls._term, formatted_timestamp)

    @classmethod
    def in_range(cls, start_value, end_value):
        """Returns a :class:`FilterGroup` to find events where the filter timestamp is in range
        between the provided `start_value` and `end_value`.
        """
        formatted_start_time = convert_timestamp_to_str(start_value)
        formatted_end_time = convert_timestamp_to_str(end_value)
        return create_in_range_filter_group(cls._term, formatted_start_time, formatted_end_time)

    @classmethod
    def on_same_day(cls, value):
        """Returns a :class:`FilterGroup` to find events where the filter timestamp is within the
        same calendar day as the provided `value`.
        """
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


class QueryFilterBooleanField(object):
    """Helper class for creating filters where the search value is a boolean."""

    _term = u"override_boolean_field_name"

    @classmethod
    def is_true(cls):
        """Returns a :class:`FilterGroup` to find events where the filter state is True."""
        return create_eq_filter_group(cls._term, u"TRUE")

    @classmethod
    def is_false(cls):
        """Returns a :class:`FilterGroup` to find events where the filter state is False."""
        return create_eq_filter_group(cls._term, u"FALSE")


class QueryFilter(object):
    """Class for constructing a single filter object for use in a Forensic Search query.

    When :func:`str()` is called on a :class:`QueryFilter` instance, the (``term``, ``operator``,
    ``value``) attribute combination is transformed into a JSON string to be used as part of a
    Forensic Search or Alert query.

    When :func:`dict()` is called on a :class:`QueryFilter` instance, the (``term``, ``operator``,
    ``value``) attribute combination is transformed into the Python `dict` equivalent of their JSON representation. This can be useful
    for programmatically manipulating a :class:`QueryFilter` after it's been created.
    """

    _term = None

    def __init__(self, term, operator, value=None):
        self._term = term
        self._operator = operator
        self._value = value

    @classmethod
    def from_dict(cls, _dict):
        return cls(_dict[u"term"], _dict[u"operator"], value=_dict.get(u"value"))

    @property
    def term(self):
        return self._term

    @property
    def operator(self):
        return self._operator

    @property
    def value(self):
        return self._value

    def __str__(self):
        value = u"null" if self._value is None else u'"{0}"'.format(self._value)
        return u'{{"operator":"{0}", "term":"{1}", "value":{2}}}'.format(
            self._operator, self._term, value
        )

    def __iter__(self):
        output_dict = {u"operator": self._operator, u"term": self._term, u"value": self._value}
        for key in output_dict:
            yield (key, output_dict[key])


class FilterGroup(object):
    """Class for constructing a logical sub-group of related filters from a list of QueryFilter
    objects. Takes a list of QueryFilter objects and combines them logically using the passed in
    filter clause (``AND`` or ``OR``).

    When :func:`str()` is called on a :class:`FilterGroup` instance, the combined filter items are
    transformed into a JSON string to be used as part of a Forensic Search or Alert query.

    When :func:`dict()` is called on a :class:`FilterGroup` instance, the combined filter items are
    transformed into the Python `dict` equivalent of their JSON representation. This can be useful
    for programmatically manipulating a :class:`FilterGroup` after it's been created.
    """

    def __init__(self, filter_list, filter_clause=u"AND"):
        self._filter_list = filter_list
        self._filter_clause = filter_clause

    @classmethod
    def from_dict(cls, _dict, filter_clause=u"AND"):
        filter_list = [QueryFilter.from_dict(item) for item in _dict[u"filters"]]
        return cls(filter_list, filter_clause=filter_clause)

    @property
    def filter_list(self):
        return self._filter_list

    @property
    def filter_clause(self):
        return self._filter_clause

    def __str__(self):
        filters_string = u",".join(str(filter_item) for filter_item in self._filter_list)
        return u'{{"filterClause":"{0}", "filters":[{1}]}}'.format(
            self._filter_clause, filters_string
        )

    def __iter__(self):
        filter_list = [dict(item) for item in self._filter_list]
        output_dict = {u"filterClause": self._filter_clause, u"filters": filter_list}
        for key in output_dict:
            yield (key, output_dict[key])

from datetime import datetime

from py42.util import convert_datetime_to_epoch
from py42.util import convert_datetime_to_timestamp_str
from py42.util import DATE_STR_FORMAT
from py42.util import parse_timestamp_to_milliseconds_precision


def create_query_filter(term, operator, value=None):
    """Creates a :class:`~py42.sdk.queries.query_filter.QueryFilter` object. Useful for
    programmatically crafting query filters, such as filters not yet defined in py42.

    Args:
        term (str): The term of the filter, such as ``actor`` or ``sharedWith``.
        operator (str): The operator between ``term`` and ``value``, such as ``IS`` or `IS_NOT`.
        value (str): The value used to filter results.

    Returns:
        :class:`~py42.sdk.queries.query_filter.QueryFilter`
    """

    return QueryFilter(term, operator, value)


def create_filter_group(query_filter_list, filter_clause):
    """Creates a :class:`~py42.sdk.queries.query_filter.FilterGroup` object. Useful for
    programmatically crafting query filters, such as filters not yet defined in py42.
    Alternatively, if you want to create custom filter groups with already defined
    operators (such as `IS` or `IS_IN`), see the other methods in this module, such as
    :meth:`~py42.sdk.queries.query_filter.create_eq_filter_group()`.

    Args:
        query_filter_list (list): a list of :class:`~py42.sdk.queries.query_filter.QueryFilter`
            objects.
        filter_clause (str): The clause joining the filters, such as ``AND`` or ``OR``.

    Returns:
        :class:`~py42.sdk.queries.query_filter.FilterGroup`
    """

    return FilterGroup(query_filter_list, filter_clause)


def create_eq_filter_group(term, value):
    """ "Creates a :class:`~py42.sdk.queries.query_filter.FilterGroup` for filtering results
    where the value with key ``term`` equals the given value. Useful for creating ``IS``
    filters that are not yet supported in py42 or programmatically crafting filter groups.

    Args:
        term: (str): The term of the filter, such as ``actor`` or ``sharedWith``.
        value (str): The value used to match on.

    Returns:
        :class:`~py42.sdk.queries.query_filter.FilterGroup`
    """

    filter_list = [create_query_filter(term, "IS", value)]
    return create_filter_group(filter_list, "AND")


def create_not_eq_filter_group(term, value):
    """ "Creates a :class:`~py42.sdk.queries.query_filter.FilterGroup` for filtering results
    where the value with key ``term`` does not equal the given value. Useful for creating
    ``IS_NOT`` filters that are not yet supported in py42 or programmatically crafting filter
    groups.

    Args:
        term: (str): The term of the filter, such as ``actor`` or ``sharedWith``.
        value (str): The value used to exclude on.

    Returns:
        :class:`~py42.sdk.queries.query_filter.FilterGroup`
    """

    filter_list = [create_query_filter(term, "IS_NOT", value)]
    return create_filter_group(filter_list, "AND")


def create_is_in_filter_group(term, value_list):
    """ "Creates a :class:`~py42.sdk.queries.query_filter.FilterGroup` for filtering results
    where the value with key ``term`` is one of several values. Useful for creating ``IS_IN``
    filters that are not yet supported in py42 or programmatically crafting filter groups.

    Args:
        term: (str): The term of the filter, such as ``actor`` or ``sharedWith``.
        value_list (list): The list of values to match on.

    Returns:
        :class:`~py42.sdk.queries.query_filter.FilterGroup`
    """

    filter_list = [create_query_filter(term, "IS", value) for value in value_list]
    return create_filter_group(filter_list, "OR" if len(filter_list) > 1 else "AND")


def create_not_in_filter_group(term, value_list):
    """ "Creates a :class:`~py42.sdk.queries.query_filter.FilterGroup` for filtering results
    where the value with key ``term`` is not one of several values. Useful for creating
    ``NOT_IN`` filters that are not yet supported in py42 or programmatically crafting
    filter groups.

    Args:
        term: (str): The term of the filter, such as ``actor`` or ``sharedWith``.
        value_list (list): The list of values to exclude on.

    Returns:
        :class:`~py42.sdk.queries.query_filter.FilterGroup`
    """

    filter_list = [create_query_filter(term, "IS_NOT", value) for value in value_list]
    return create_filter_group(filter_list, "AND")


def create_on_or_after_filter_group(term, value):
    """ "Creates a :class:`~py42.sdk.queries.query_filter.FilterGroup` for filtering results
    where the value with key ``term`` is on or after the given value. Examples include
    values describing dates. Useful for creating ``ON_OR_AFTER`` filters that are not yet
    supported in py42  or programmatically crafting filter groups.

    Args:
        term: (str): The term of the filter, such as ``eventTimestamp``.
        value (str or int): The value used to filter results.

    Returns:
        :class:`~py42.sdk.queries.query_filter.FilterGroup`
    """

    filter_list = [create_query_filter(term, "ON_OR_AFTER", value)]
    return create_filter_group(filter_list, "AND")


def create_on_or_before_filter_group(term, value):
    """ "Creates a :class:`~py42.sdk.queries.query_filter.FilterGroup` for filtering results
    where the value with key ``term`` is on or before the given value. Examples include
    values describing dates. Useful for creating ``ON_OR_BEFORE`` filters that are not
    yet supported in py42 or programmatically crafting filter groups.

    Args:
        term: (str): The term of the filter, such as ``eventTimestamp``.
        value (str or int): The value used to filter results.

    Returns:
        :class:`~py42.sdk.queries.query_filter.FilterGroup`
    """

    filter_list = [create_query_filter(term, "ON_OR_BEFORE", value)]
    return create_filter_group(filter_list, "AND")


def create_in_range_filter_group(term, start_value, end_value):
    """ "Creates a :class:`~py42.sdk.queries.query_filter.FilterGroup` for filtering results
    where the value with key ``term`` is in the given range. Examples include values describing
    dates. Useful for creating a combination of ``ON_OR_AFTER`` and ``ON_OR_BEFORE`` filters
    that are not yet supported in py42 or programmatically crafting filter groups.

    Args:
        term: (str): The term of the filter, such as ``eventTimestamp``.
        start_value (str or int): The start value used to filter results.
        end_value (str or int): The end value used to filter results.

    Returns:
        :class:`~py42.sdk.queries.query_filter.FilterGroup`
    """

    filter_list = [
        create_query_filter(term, "ON_OR_AFTER", start_value),
        create_query_filter(term, "ON_OR_BEFORE", end_value),
    ]
    return create_filter_group(filter_list, "AND")


def create_within_the_last_filter_group(term, value):
    """Returns a :class:`~py42.sdk.queries.query_filter.FilterGroup` that is useful
    for finding results where the key ``term`` is an ``EventTimestamp._term``
    and the value is one of the `EventTimestamp` attributes as `value`.

    Args:
        value (str): `EventTimestamp` attribute.

    Returns:
        :class:`~py42.sdk.queries.query_filter.FilterGroup`
    """
    filter_list = [create_query_filter(term, "WITHIN_THE_LAST", value)]
    return create_filter_group(filter_list, "AND")


class QueryFilterStringField:
    """Helper class for creating filters where the search value is a string."""

    _term = "override_string_field_name"

    @classmethod
    def eq(cls, value):
        """Returns a :class:`~py42.sdk.queries.query_filter.FilterGroup` that is useful
        for finding results where the value with key ``self._term`` equals the provided
        ``value``.

        Args:
            value (str): The value to match on.

        Returns:
            :class:`~py42.sdk.queries.query_filter.FilterGroup`
        """
        return create_eq_filter_group(cls._term, value)

    @classmethod
    def not_eq(cls, value):
        """Returns a :class:`~py42.sdk.queries.query_filter.FilterGroup` that is useful
        for finding results where the value with key ``self._term`` does not equal the provided ``value``.

        Args:
            value (str): The value to exclude on.

        Returns:
            :class:`~py42.sdk.queries.query_filter.FilterGroup`
        """
        return create_not_eq_filter_group(cls._term, value)

    @classmethod
    def is_in(cls, value_list):
        """Returns a :class:`~py42.sdk.queries.query_filter.FilterGroup` that is useful
        for finding results where the value with the key ``self._term`` is in the provided
        ``value_list``.

        Args:
            value_list (list): The list of values to match on.

        Returns:
            :class:`~py42.sdk.queries.query_filter.FilterGroup`
        """
        return create_is_in_filter_group(cls._term, value_list)

    @classmethod
    def not_in(cls, value_list):
        """Returns a :class:`~py42.sdk.queries.query_filter.FilterGroup` that is useful
        for finding results where the value with the key ``self._term`` is not in the provided
        ``value_list``.

        Args:
            value_list (list): The list of values to exclude on.

        Returns:
            :class:`~py42.sdk.queries.query_filter.FilterGroup`
        """
        return create_not_in_filter_group(cls._term, value_list)


class QueryFilterTimestampField:
    """Helper class for creating filters where the search value is a timestamp."""

    _term = "override_timestamp_field_name"

    @staticmethod
    def _parse_timestamp(value):
        return parse_timestamp_to_milliseconds_precision(value)

    @staticmethod
    def _convert_datetime_to_timestamp(value):
        return convert_datetime_to_timestamp_str(value)

    @classmethod
    def on_or_after(cls, value):
        """Returns a :class:`~py42.sdk.queries.query_filter.FilterGroup` that is useful
        for finding results where the value with key ``self._term` is on or after the
        provided ``value``.

        Args:
            value (str or int or float or datetime): The value used to filter results.

        Returns:
            :class:`~py42.sdk.queries.query_filter.FilterGroup`
        """
        formatted_timestamp = cls._parse_timestamp(value)
        return create_on_or_after_filter_group(cls._term, formatted_timestamp)

    @classmethod
    def on_or_before(cls, value):
        """Returns a :class:`~py42.sdk.queries.query_filter.FilterGroup` that is useful
        for finding results where the value with key ``self._term`` is on or before the
        provided ``value``.

        Args:
            value (str or int or float or datetime): The value used to filter results.

        Returns:
            :class:`~py42.sdk.queries.query_filter.FilterGroup`
        """
        formatted_timestamp = cls._parse_timestamp(value)
        return create_on_or_before_filter_group(cls._term, formatted_timestamp)

    @classmethod
    def in_range(cls, start_value, end_value):
        """Returns a :class:`~py42.sdk.queries.query_filter.FilterGroup` that is useful
        for finding results where the value with key ``self._term`` is in range between
        the provided ``start_value`` and ``end_value``.

        Args:
            start_value (str or int or float or datetime): The start value used to
                filter results.
            end_value (str or int or float or datetime): The end value used to
                filter results.

        Returns:
            :class:`~py42.sdk.queries.query_filter.FilterGroup`
        """
        formatted_start_time = cls._parse_timestamp(start_value)
        formatted_end_time = cls._parse_timestamp(end_value)
        return create_in_range_filter_group(
            cls._term, formatted_start_time, formatted_end_time
        )

    @classmethod
    def on_same_day(cls, value):
        """Returns a :class:`~py42.sdk.queries.query_filter.FilterGroup` that is useful
        for finding results where the value with key ``self._term`` is within the same
        calendar day as the provided ``value``.

        Args:
            value (str or int or float or datetime): The value used to filter results.

        Returns:
            :class:`~py42.sdk.queries.query_filter.FilterGroup`
        """
        if isinstance(value, str):
            value = convert_datetime_to_epoch(datetime.strptime(value, DATE_STR_FORMAT))
        elif isinstance(value, datetime):
            value = convert_datetime_to_epoch(value)
        date_from_value = datetime.utcfromtimestamp(value)
        start_time = datetime(
            date_from_value.year, date_from_value.month, date_from_value.day, 0, 0, 0
        )
        end_time = datetime(
            date_from_value.year, date_from_value.month, date_from_value.day, 23, 59, 59
        )
        formatted_start_time = cls._convert_datetime_to_timestamp(start_time)
        formatted_end_time = cls._convert_datetime_to_timestamp(end_time)
        return create_in_range_filter_group(
            cls._term, formatted_start_time, formatted_end_time
        )


class QueryFilterBooleanField:
    """Helper class for creating filters where the search value is a boolean."""

    _term = "override_boolean_field_name"

    @classmethod
    def is_true(cls):
        """Returns a :class:`~py42.sdk.queries.query_filter.FilterGroup` that is useful
        for finding results where the value with key ``self._term`` is True.

        Returns:
            :class:`~py42.sdk.queries.query_filter.FilterGroup`
        """
        return create_eq_filter_group(cls._term, "TRUE")

    @classmethod
    def is_false(cls):
        """Returns a :class:`~py42.sdk.queries.query_filter.FilterGroup` that is useful
        for finding results where the value with key ``self._term`` is False.

        Returns:
            :class:`~py42.sdk.queries.query_filter.FilterGroup`
        """
        return create_eq_filter_group(cls._term, "FALSE")


class QueryFilter:
    """Class for constructing a single filter object for use in a search query.

    When :func:`str()` is called on a :class:`~py42.sdk.queries.query_filter.QueryFilter`
    instance, the (``term``, ``operator``, ``value``) attribute combination is transformed
    into a JSON string to be used as part of a Forensic Search or Alert query.

    When :func:`dict()` is called on a :class:`~py42.sdk.queries.query_filter.QueryFilter`
    instance, the (``term``, ``operator``, ``value``) attribute combination is transformed
    into the Python `dict` equivalent of their JSON representation. This can be useful
    for programmatically manipulating a :class:`~py42.sdk.queries.query_filter.QueryFilter`
    after it's been created.
    """

    _term = None

    def __init__(self, term, operator, value=None):
        self._term = term
        self._operator = operator
        self._value = value

    @classmethod
    def from_dict(cls, _dict):
        """Creates an instance of :class:`~py42.sdk.queries.query_filter.QueryFilter` from
        the values found in ``_dict``. ``_dict`` must contain keys ``term``, ``operator``,
        and ``value``.

        Args:
            _dict (dict): A dictionary containing keys ``term``, ``operator``, and ``value``.

        Returns:
            :class:`~py42.sdk.queries.query_filter.QueryFilter`
        """

        return cls(_dict["term"], _dict["operator"], value=_dict.get("value"))

    @property
    def term(self):
        """The term of the filter, such as ``actor`` or ``sharedWith``."""

        return self._term

    @property
    def operator(self):
        """The operator between ``term`` and ``value``, such as ``IS`` or `IS_NOT`."""

        return self._operator

    @property
    def value(self):
        """The value used to filter results."""

        return self._value

    def __str__(self):
        value = "null" if self._value is None else f'"{self._value}"'
        return (
            f'{{"operator":"{self._operator}", "term":"{self._term}", "value":{value}}}'
        )

    def __iter__(self):
        output_dict = {
            "operator": self._operator,
            "term": self._term,
            "value": self._value,
        }
        for key in output_dict:
            yield key, output_dict[key]

    def __eq__(self, other):
        if isinstance(other, (QueryFilter, tuple, list)):
            return tuple(self) == tuple(other)
        elif isinstance(other, str):
            return str(self) == other
        else:
            return False

    def __hash__(self):
        return hash(str(self))


class FilterGroup:
    """Class for constructing a logical sub-group of related filters from a list of
    :class:`~py42.sdk.queries.query_filter.QueryFilter` objects. Takes a list of
    :class:`~py42.sdk.queries.query_filter.QueryFilter` objects and combines them
    logically using the passed in filter clause (``AND`` or ``OR``).

    When :func:`str()` is called on a :class:`FilterGroup` instance, the combined filter items are
    transformed into a JSON string to be used as part of a Forensic Search or Alert query.

    When :func:`dict()` is called on a :class:`~py42.sdk.queries.query_filter.FilterGroup`
    instance, the combined filter items are transformed into the Python `dict` equivalent
    of their JSON representation. This can be useful for programmatically manipulating a
    :class:`~py42.sdk.queries.query_filter.FilterGroup` after it's been created.
    """

    def __init__(self, filter_list, filter_clause="AND"):
        self._filter_list = filter_list
        self._filter_clause = filter_clause

    @classmethod
    def from_dict(cls, _dict):
        """Creates an instance of :class:`~py42.sdk.queries.query_filter.FilterGroup`
        from the values found in ``_dict``. ``_dict`` must contain keys ``filters`` and
        ``filterClause``.

        Args:
            _dict (dict): A dictionary containing keys ``term``, ``operator``, and ``value``.

        Returns:
            :class:`~py42.sdk.queries.query_filter.FilterGroup`
        """
        filter_list = [QueryFilter.from_dict(item) for item in _dict["filters"]]
        return cls(filter_list, filter_clause=_dict["filterClause"])

    @property
    def filter_list(self):
        """The list of :class:`~py42.sdk.queries.query_filter.QueryFilter` objects in this
        group."""

        return self._filter_list

    @property
    def filter_clause(self):
        """The clause joining the filters, such as ``AND`` or ``OR``."""

        return self._filter_clause

    @filter_clause.setter
    def filter_clause(self, value):
        """The clause joining the filters, such as ``AND`` or ``OR``."""

        self._filter_clause = value

    @property
    def _filter_set(self):
        return sorted(list(set(self.filter_list)), key=str)

    def __str__(self):
        filters_string = ",".join(str(filter_item) for filter_item in self._filter_set)
        return (
            f'{{"filterClause":"{self._filter_clause}", "filters":[{filters_string}]}}'
        )

    def __iter__(self):
        filter_list = [dict(item) for item in self._filter_set]
        output_dict = {"filterClause": self._filter_clause, "filters": filter_list}
        for key in output_dict:
            yield key, output_dict[key]

    def __eq__(self, other):
        if isinstance(other, FilterGroup):
            return (
                self.filter_clause == other.filter_clause
                and self._filter_set == other._filter_set
            )
        elif isinstance(other, (tuple, list)):
            return tuple(self) == tuple(other)
        elif isinstance(other, str):
            return str(self) == other
        else:
            return False

    def __contains__(self, item):
        return item in self._filter_set

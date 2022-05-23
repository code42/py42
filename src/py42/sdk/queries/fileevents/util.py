from py42.sdk.queries.query_filter import create_filter_group
from py42.sdk.queries.query_filter import create_query_filter
from py42.sdk.queries.query_filter import create_within_the_last_filter_group
from py42.sdk.queries.query_filter import QueryFilterStringField
from py42.sdk.queries.query_filter import QueryFilterTimestampField


def create_exists_filter_group(term):
    """Creates a :class:`~py42.sdk.queries.query_filter.FilterGroup` to find events where
    filter data exists. Useful for creating ``EXISTS`` filters that are not yet supported
    in py42 or programmatically crafting filter groups.

    Args:
        term (str): The term of the filter.

    Returns:
        :class:`~py42.sdk.queries.query_filter.FilterGroup`
    """
    filter_list = [create_query_filter(term, "EXISTS")]
    return create_filter_group(filter_list, "AND")


def create_not_exists_filter_group(term):
    """Creates a :class:`~py42.sdk.queries.query_filter.FilterGroup` to find events where
    filter data does not exist. Useful for creating ``DOES_NOT_EXIST`` filters that are
    not yet supported in py42 or programmatically crafting filter groups.

    Args:
        term (str): The term of the filter.

    Returns:
        :class:`~py42.sdk.queries.query_filter.FilterGroup`
    """
    filter_list = [create_query_filter(term, "DOES_NOT_EXIST")]
    return create_filter_group(filter_list, "AND")


def create_greater_than_filter_group(term, value):
    """Creates a :class:`~py42.sdk.queries.query_filter.FilterGroup` for matching file
    events where the value with key ``term`` is greater than the given value. Useful for
    creating ``GREATER_THAN`` filters that are not yet supported in py42 or programmatically
    crafting filter groups.

    Args:
        term (str): The term of the filter.
        value (str or int): The value used to filter file events.

    Returns:
        :class:`~py42.sdk.queries.query_filter.FilterGroup`
    """
    filter_list = [create_query_filter(term, "GREATER_THAN", value)]
    return create_filter_group(filter_list, "AND")


def create_less_than_filter_group(term, value):
    """Creates a :class:`~py42.sdk.queries.query_filter.FilterGroup` for matching file
    events where the value with key ``term`` is less than the given value. Useful for creating
    ``LESS_THAN`` filters that are not yet supported in py42 or programmatically crafting
    filter groups.

    Args:
        term (str): The term of the filter.
        value (str or int): The value used to filter file events.

    Returns:
        :class:`~py42.sdk.queries.query_filter.FilterGroup`
    """
    filter_list = [create_query_filter(term, "LESS_THAN", value)]
    return create_filter_group(filter_list, "AND")


class FileEventFilterStringField(QueryFilterStringField):
    """Helper class for creating filters with the ``EXISTS``/``NOT_EXISTS`` filter clauses."""

    @classmethod
    def exists(cls):
        """Returns a :class:`~py42.sdk.queries.query_filter.FilterGroup` to find events
        where filter data exists.

        Returns:
            :class:`~py42.sdk.queries.query_filter.FilterGroup`
        """
        return create_exists_filter_group(cls._term)

    @classmethod
    def not_exists(cls):
        """Returns a :class:`~py42.sdk.queries.query_filter.FilterGroup` to find events
        where filter data does not exist.

        Returns:
            :class:`~py42.sdk.queries.query_filter.FilterGroup`
        """
        return create_not_exists_filter_group(cls._term)


class FileEventFilterComparableField:
    """Helper class for creating filters with the ``GREATER_THAN``/``LESS_THAN`` filter clauses."""

    _term = "override_boolean_field_name"

    @classmethod
    def greater_than(cls, value):
        """Returns a :class:`~py42.sdk.queries.query_filter.FilterGroup` to find events
        where filter data is greater than the provided value.

        Args:
            value (str or int or float): The value used to filter file events.

        Returns:
            :class:`~py42.sdk.queries.query_filter.FilterGroup`
        """
        value = int(value)
        return create_greater_than_filter_group(cls._term, value)

    @classmethod
    def less_than(cls, value):
        """Returns a :class:`~py42.sdk.queries.query_filter.FilterGroup` to find events
        where filter data is less than than the provided value.

        Args:
            value (str or int or float): The value used to filter file events.

        Returns:
            :class:`~py42.sdk.queries.query_filter.FilterGroup`
        """
        value = int(value)
        return create_less_than_filter_group(cls._term, value)


class FileEventFilterTimestampField(QueryFilterTimestampField):
    @classmethod
    def within_the_last(cls, value):
        """Returns a :class:`~py42.sdk.queries.query_filter.FilterGroup` that is useful
        for finding results where the key ``self._term`` is a timestamp-related term,
        such as ``EventTimestamp._term``, and ``value`` is one of it's accepted values,
        such as one of the values in ``EventTimestamp.choices()``.

        Args:
            value (str): The value used to filter file events.

        Returns:
            :class:`~py42.sdk.queries.query_filter.FilterGroup`
        """
        return create_within_the_last_filter_group(cls._term, value)

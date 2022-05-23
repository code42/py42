from py42.sdk.queries.query_filter import create_filter_group
from py42.sdk.queries.query_filter import create_query_filter
from py42.sdk.queries.query_filter import QueryFilterStringField
from py42.sdk.queries.query_filter import QueryFilterTimestampField
from py42.util import MICROSECOND_FORMAT
from py42.util import parse_timestamp_to_microseconds_precision


def create_contains_filter_group(term, value):
    """Creates a :class:`~py42.sdk.queries.query_filter.FilterGroup` for filtering results
    where the value with key ``term`` contains the given value. Useful for creating ``CONTAINS``
    filters that are not yet supported in py42 or programmatically crafting filter groups.

    Args:
        term: (str): The term of the filter, such as ``actor``.
        value (str): The value used to match on.

    Returns:
        :class:`~py42.sdk.queries.query_filter.FilterGroup`
    """

    filter_list = [create_query_filter(term, "CONTAINS", value)]
    return create_filter_group(filter_list, "AND")


def create_not_contains_filter_group(term, value):
    """Creates a :class:`~py42.sdk.queries.query_filter.FilterGroup` for filtering results
    where the value with key ``term`` does not contain the given value. Useful for creating
    ``DOES_NOT_CONTAIN`` filters that are not yet supported in py42 or programmatically
    crafting filter groups.

    Args:
        term: (str): The term of the filter, such as ``actor``.
        value (str): The value used to exclude on.

    Returns:
        :class:`~py42.sdk.queries.query_filter.FilterGroup`
    """

    filter_list = [create_query_filter(term, "DOES_NOT_CONTAIN", value)]
    return create_filter_group(filter_list, "AND")


class AlertQueryFilterStringField(QueryFilterStringField):
    @classmethod
    def contains(cls, value):
        """Creates a :class:`~py42.sdk.queries.query_filter.FilterGroup` for filtering
        results where the value with key ``self._term`` contains the given value. Useful
        for creating ``CONTAINS`` filters that are not yet supported in py42 or programmatically
        crafting filter groups.

        Args:
            value (str): The value used to match on.

        Returns:
            :class:`~py42.sdk.queries.query_filter.FilterGroup`
        """

        return create_contains_filter_group(cls._term, value)

    @classmethod
    def not_contains(cls, value):
        """Creates a :class:`~py42.sdk.queries.query_filter.FilterGroup` for filtering
        results where the value with key ``self._term`` does not contain the given value.
        Useful for creating ``DOES_NOT_CONTAIN`` filters that are not yet supported in py42
        or programmatically crafting filter groups.

        Args:
            value (str): The value used to exclude on.

        Returns:
            :class:`~py42.sdk.queries.query_filter.FilterGroup`
        """

        return create_not_contains_filter_group(cls._term, value)


class AlertQueryFilterTimestampField(QueryFilterTimestampField):
    """Helper class for creating alert filters where the search value is a timestamp."""

    @staticmethod
    def _parse_timestamp(value):
        return parse_timestamp_to_microseconds_precision(value)

    @staticmethod
    def _convert_datetime_to_timestamp(value):
        return value.strftime(MICROSECOND_FORMAT)

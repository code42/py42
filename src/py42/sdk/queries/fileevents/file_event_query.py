from py42.sdk.queries import BaseQuery
from py42.sdk.queries.query_filter import create_filter_group
from py42.sdk.queries.query_filter import create_query_filter
from py42.sdk.queries.query_filter import create_within_the_last_filter_group
from py42.sdk.queries.query_filter import QueryFilterStringField
from py42.sdk.queries.query_filter import QueryFilterTimestampField


class FileEventQuery(BaseQuery):
    """Helper class for building Code42 Forensic Search queries.

    A FileEventQuery instance's ``all()`` and ``any()`` take one or more
    :class:`~py42.sdk.queries.query_filter.FilterGroup` objects to construct a query that
    can be passed to the :meth:`FileEventService.search()` method. ``all()`` returns results
    that match all of the provided filter criteria, ``any()`` will return results that
    match any of the filters.

    For convenience, the :class:`FileEventQuery` constructor does the same as ``all()``.

    Usage example::

        email_filter = EmailSender.is_in(["test.user@example.com", "test.sender@example.com"])
        exposure_filter = ExposureType.exists()
        query = FileEventQuery.all(email_filter, exposure_filter)

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sort_key = "eventId"

    def __str__(self):
        groups_string = ",".join(
            str(group_item) for group_item in self._filter_group_list
        )
        if self.page_token is not None:
            paging_prop = f'"srtDir":"{self.sort_direction}", "srtKey":"{self.sort_key}", "pgToken":"{self.page_token}"'
        else:
            paging_prop = f'"srtDir":"{self.sort_direction}", "srtKey":"{self.sort_key}", "pgNum":{self.page_number}'
        json = f'{{"groupClause":"{self._group_clause}", "groups":[{groups_string}], {paging_prop}, "pgSize":{self.page_size}}}'
        return json

    def __iter__(self):
        filter_group_list = [dict(item) for item in self._filter_group_list]
        output_dict = {
            "groupClause": self._group_clause,
            "groups": filter_group_list,
            "pgSize": self.page_size,
            "srtDir": self.sort_direction,
            "srtKey": self.sort_key,
        }

        if self.page_token is not None:
            output_dict["pgToken"] = self.page_token
        else:
            output_dict["pgNum"] = self.page_number

        for key in output_dict:
            yield key, output_dict[key]


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

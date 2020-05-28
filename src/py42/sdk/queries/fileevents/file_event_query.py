from py42._internal.compat import str
from py42.sdk.queries import BaseQuery
from py42.sdk.queries.query_filter import (
    QueryFilterStringField,
    create_filter_group,
    create_query_filter,
)


class FileEventQuery(BaseQuery):
    """Helper class for building Code42 Forensic Search queries.

    A FileEventQuery instance's ``all()`` and ``any()`` take one or more :class:`FilterGroup`
    objects to construct a query that can be passed to the :meth:`FileEventClient.search()` method.
    ``all()`` returns results that match all of the provided filter criteria, ``any()`` will return
    results that match any of the filters.

    For convenience, the :class:`FileEventQuery` constructor does the same as ``all()``.

    Usage example::

        email_filter = EmailSender.is_in(["test.user@example.com", "test.sender@example.com"])
        exposure_filter = ExposureType.exists()

        query = FileEventQuery.all(email_filter, exposure_filter)

    """

    def __init__(self, *args, **kwargs):
        super(FileEventQuery, self).__init__(*args, **kwargs)
        self.sort_key = u"eventId"
        self.page_number = 1

    def __str__(self):
        groups_string = u",".join(str(group_item) for group_item in self._filter_group_list)
        json = u'{{"groupClause":"{0}", "groups":[{1}], "pgNum":{2}, "pgSize":{3}, "srtDir":"{4}", "srtKey":"{5}"}}'.format(
            self._group_clause,
            groups_string,
            self.page_number,
            self.page_size,
            self.sort_direction,
            self.sort_key,
        )
        return json

    def __iter__(self):
        filter_group_list = [dict(item) for item in self._filter_group_list]
        output_dict = {
            u"groupClause": self._group_clause,
            u"groups": filter_group_list,
            u"pgNum": self.page_number,
            u"pgSize": self.page_size,
            u"srtDir": self.sort_direction,
            u"srtKey": self.sort_key,
        }
        for key in output_dict:
            yield (key, output_dict[key])


def create_exists_filter_group(term):
    filter_list = [create_query_filter(term, u"EXISTS")]
    return create_filter_group(filter_list, u"AND")


def create_not_exists_filter_group(term):
    filter_list = [create_query_filter(term, u"DOES_NOT_EXIST")]
    return create_filter_group(filter_list, u"AND")


def create_greater_than_filter_group(term, value):
    filter_list = [create_query_filter(term, u"GREATER_THAN", value)]
    return create_filter_group(filter_list, u"AND")


def create_less_than_filter_group(term, value):
    filter_list = [create_query_filter(term, u"LESS_THAN", value)]
    return create_filter_group(filter_list, u"AND")


class FileEventFilterStringField(QueryFilterStringField):
    """Helper class for creating filters with the ``EXISTS``/``NOT_EXISTS`` filter clauses."""

    @classmethod
    def exists(cls):
        """Returns a :class:`FilterGroup` to find events where filter data exists."""
        return create_exists_filter_group(cls._term)

    @classmethod
    def not_exists(cls):
        """Returns a :class:`FilterGroup` to find events where filter data does not exist."""
        return create_not_exists_filter_group(cls._term)


class FileEventFilterComparableField(object):
    """Helper class for creating filters with the ``GREATER_THAN``/``LESS_THAN`` filter clauses."""

    _term = u"override_boolean_field_name"

    @classmethod
    def greater_than(cls, value):
        """Returns a :class:`FilterGroup` to find events where filter data is greater than the
        provided value.
        """
        value = int(value)
        return create_greater_than_filter_group(cls._term, value)

    @classmethod
    def less_than(cls, value):
        """Returns a :class:`FilterGroup` to find events where filter data is less than than the
        provided value.
        """
        value = int(value)
        return create_less_than_filter_group(cls._term, value)
